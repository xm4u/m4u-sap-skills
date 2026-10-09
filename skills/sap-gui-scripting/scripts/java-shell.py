#!/usr/bin/env python3
"""Submit one script to a bridge already loaded in SAP GUI for Java. Stdlib only."""

import argparse
import json
import os
from pathlib import Path
import sys
import time
import uuid


class BridgeError(Exception):
    pass


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def private_directory(root):
    if root.is_symlink() or not root.is_dir():
        raise BridgeError("Bridge directory is missing or a symlink; load java-shell-bridge.js in SAP GUI first.")
    stat = root.stat()
    if stat.st_uid != os.getuid() or stat.st_mode & 0o077:
        raise BridgeError("Bridge directory must belong to this user and have mode 0700.")


def bridge_state(root, freshness=5):
    try:
        state = read_json(root / "bridge.json")
    except (OSError, ValueError) as error:
        raise BridgeError("Cannot read bridge state; load java-shell-bridge.js in the authenticated SAP instance.") from error
    if state.get("schema") != "sap-gui-java-bridge/v1" or not state.get("instanceId"):
        raise BridgeError("Invalid bridge state.")
    if state.get("stopped"):
        raise BridgeError("Bridge is stopped: " + state.get("error", "load it again in SAP GUI"))
    if time.time() * 1000 - state.get("heartbeatAt", 0) > freshness * 1000:
        raise BridgeError("Bridge heartbeat is stale or a script is busy. Inspect SAP and pending files; do not restart or retry blindly.")
    return state


def submit(root, operation, source, timeout):
    private_directory(root)
    state = bridge_state(root)
    lock = root / "client.lock"
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError as error:
        raise BridgeError("Another or unresolved request owns client.lock. Inspect its requestId and SAP state before continuing.") from error
    request_id = uuid.uuid4().hex
    request = {"requestId": request_id, "instanceId": state["instanceId"], "operation": operation}
    if source is not None:
        request["source"] = source
    raw = json.dumps(request, ensure_ascii=True).encode("utf-8")
    submitted = False
    completed = False
    response_path = root / ("response-" + request_id + ".json")
    temporary = root / ("request-" + request_id + ".tmp")
    try:
        (lock / "request.json").write_text(json.dumps({"requestId": request_id, "pid": os.getpid()}), encoding="utf-8")
        if len(raw) > 1048576:
            raise BridgeError("Request exceeds 1 MiB.")
        if (root / "request.json").exists() or (root / "running.json").exists():
            raise BridgeError("A pending request exists. Inspect SAP and the request before continuing.")
        # Recheck after taking the lock; a bridge restart cannot inherit this request.
        if bridge_state(root)["instanceId"] != state["instanceId"]:
            raise BridgeError("Bridge changed before submission; inspect the new instance.")
        with temporary.open("xb") as handle:
            os.chmod(temporary, 0o600)
            handle.write(raw)
        os.replace(temporary, root / "request.json")
        submitted = True
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if response_path.exists():
                response = read_json(response_path)
                if (response.get("schema") != "sap-gui-java-shell/v1"
                        or response.get("requestId") != request_id
                        or response.get("instanceId") != state["instanceId"]
                        or not isinstance(response.get("ok"), bool)):
                    raise BridgeError("Response identity/schema mismatch; request outcome is uncertain.")
                # The server removes its running marker after publishing the response.
                if (root / "running.json").exists():
                    time.sleep(0.05)
                    continue
                completed = True
                response_path.unlink()
                return response
            time.sleep(0.1)
        raise BridgeError("Timed out; execution may still finish. Do not retry. Inspect SAP and response-"
                          + request_id + ".json. client.lock is retained for diagnosis.")
    finally:
        if temporary.exists():
            temporary.unlink()
        if not submitted or completed:
            (lock / "request.json").unlink(missing_ok=True)
            lock.rmdir()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bridge-dir", type=Path, default=Path.home() / "scripts" / "sap-gui-shell-bridge")
    parser.add_argument("--timeout", type=float, default=30, help="Wait in seconds; timeout never cancels/replays a SAP action")
    command = parser.add_mutually_exclusive_group(required=True)
    command.add_argument("--script", type=Path, help="An ES5-compatible SAP GUI Java script; its final value becomes result")
    command.add_argument("--status", action="store_true")
    command.add_argument("--stop", action="store_true", help="Stop only the bridge, leaving SAP and its sessions open")
    args = parser.parse_args(argv)
    try:
        if not 0 < args.timeout <= 300:
            raise BridgeError("Use a timeout greater than 0 and at most 300 seconds.")
        source = args.script.read_text(encoding="utf-8") if args.script else None
        operation = "run" if args.script else "stop" if args.stop else "status"
        response = submit(args.bridge_dir.expanduser().absolute(), operation, source, args.timeout)
        print(json.dumps(response, ensure_ascii=False))
        return 0 if response["ok"] else 1
    except (BridgeError, OSError, ValueError) as error:
        print(json.dumps({"schema": "sap-gui-java-shell/v1", "ok": False, "transportError": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
