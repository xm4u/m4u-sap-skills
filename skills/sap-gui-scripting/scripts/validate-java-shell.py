#!/usr/bin/env python3
"""Local protocol fixtures. Never connect to SAP or start its client."""
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest

spec = importlib.util.spec_from_file_location("java_shell", Path(__file__).with_name("java-shell.py"))
shell = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shell)


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="sap-java-shell-fixture-")
        self.root = Path(self.temporary.name)
        self.root.chmod(0o700)
        self.instance = "fixture-instance"
        self.write_state()

    def tearDown(self):
        self.temporary.cleanup()

    def write_state(self, **overrides):
        state = {"schema": "sap-gui-java-bridge/v1", "instanceId": self.instance,
                 "heartbeatAt": time.time() * 1000, "stopped": False}
        state.update(overrides)
        (self.root / "bridge.json").write_text(json.dumps(state))

    def server(self, ok=True, mismatch=False):
        seen = []
        def respond():
            deadline = time.monotonic() + 2
            while not (self.root / "request.json").exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            request_path = self.root / "request.json"
            if not request_path.exists():
                return
            request = json.loads(request_path.read_text())
            seen.append(request)
            request_path.rename(self.root / "running.json")
            response = {"schema": "sap-gui-java-shell/v1", "instanceId": self.instance,
                        "requestId": "wrong" if mismatch else request["requestId"], "ok": ok}
            if ok:
                response["result"] = {"phase": "observed"}
            else:
                response["error"] = "SAP rejected the action"
            path = self.root / ("response-" + request["requestId"] + ".json")
            pending = path.with_suffix(".tmp")
            pending.write_text(json.dumps(response))
            pending.rename(path)
            (self.root / "running.json").unlink()
        worker = threading.Thread(target=respond)
        worker.start()
        self.addCleanup(worker.join)
        return seen, worker

    def test_complete_request_returns_result_and_releases_lock(self):
        seen, worker = self.server()
        response = shell.submit(self.root, "run", '"source with quotes and \\n"', 1)
        worker.join()
        self.assertTrue(response["ok"])
        self.assertEqual(response["result"], {"phase": "observed"})
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0]["source"], '"source with quotes and \\n"')
        self.assertFalse((self.root / "client.lock").exists())
        self.assertFalse(list(self.root.glob("response-*.json")))

    def test_script_failure_is_returned_without_resubmitting(self):
        seen, worker = self.server(ok=False)
        response = shell.submit(self.root, "run", "throw new Error('failure')", 1)
        worker.join()
        self.assertFalse(response["ok"])
        self.assertEqual(len(seen), 1)
        self.assertFalse((self.root / "client.lock").exists())

    def test_timeout_keeps_single_request_and_diagnostic_lock(self):
        with self.assertRaisesRegex(shell.BridgeError, "Do not retry"):
            shell.submit(self.root, "run", "authorized-action", 0.05)
        request = json.loads((self.root / "request.json").read_text())
        self.assertEqual(request["source"], "authorized-action")
        with self.assertRaisesRegex(shell.BridgeError, "client.lock"):
            shell.submit(self.root, "run", "must-not-run", 0.05)
        self.assertEqual(json.loads((self.root / "request.json").read_text()), request)

    def test_mismatched_response_keeps_diagnostic_lock(self):
        self.server(mismatch=True)
        with self.assertRaisesRegex(shell.BridgeError, "mismatch"):
            shell.submit(self.root, "status", None, 1)
        self.assertTrue((self.root / "client.lock").exists())

    def test_stale_and_stopped_bridges_refuse_submission(self):
        for override in [{"heartbeatAt": 0}, {"stopped": True}]:
            self.write_state(**override)
            with self.assertRaises(shell.BridgeError):
                shell.submit(self.root, "run", "must-not-run", 0.05)
            self.assertFalse((self.root / "request.json").exists())

    def test_pending_request_is_preserved(self):
        pending = self.root / "running.json"
        pending.write_text('{"requestId":"existing"}')
        with self.assertRaisesRegex(shell.BridgeError, "pending"):
            shell.submit(self.root, "run", "must-not-run", 0.05)
        self.assertEqual(pending.read_text(), '{"requestId":"existing"}')
        self.assertFalse((self.root / "client.lock").exists())

    def test_shared_directory_is_rejected(self):
        self.root.chmod(0o755)
        with self.assertRaisesRegex(shell.BridgeError, "0700"):
            shell.submit(self.root, "status", None, 0.05)

    def test_symlink_directory_is_rejected(self):
        link = self.root / "alias"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(shell.BridgeError, "symlink"):
            shell.submit(link, "status", None, 0.05)

    def test_oversized_source_never_reaches_server(self):
        with self.assertRaisesRegex(shell.BridgeError, "1 MiB"):
            shell.submit(self.root, "run", "x" * 1048576, 0.05)
        self.assertFalse((self.root / "request.json").exists())
        self.assertFalse((self.root / "client.lock").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
