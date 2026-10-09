#!/usr/bin/env python3
"""Start SAP GUI for Java with its bridge, or submit scripts through it. Stdlib only."""

import argparse
import json
import os
from pathlib import Path
import sys
import subprocess
import time
import uuid


class BridgeError(Exception):
    pass


def read_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise BridgeError("Expected a JSON object in " + str(path))
    return value


def private_directory(root):
    if root.is_symlink() or not root.is_dir():
        raise BridgeError("Bridge directory is missing or a symlink; use java-shell.py --start first.")
    stat = root.stat()
    if stat.st_uid != os.getuid() or stat.st_mode & 0o077:
        raise BridgeError("Bridge directory must belong to this user and have mode 0700.")


def bridge_state(root, freshness=5):
    try:
        state = read_json(root / "bridge.json")
    except (OSError, ValueError) as error:
        raise BridgeError("Cannot read bridge state; use java-shell.py --start first.") from error
    if (state.get("schema") != "sap-gui-java-bridge/v1"
            or not isinstance(state.get("instanceId"), str) or not state["instanceId"]
            or isinstance(state.get("heartbeatAt"), bool)
            or not isinstance(state.get("heartbeatAt"), (int, float))):
        raise BridgeError("Invalid bridge state.")
    owner_path = root / "owner.json"
    if owner_path.exists():
        owner = read_json(owner_path)
        if owner.get("instanceId") != state["instanceId"]:
            raise BridgeError("Bridge state and process owner disagree; inspect them before continuing.")
        state.setdefault("processId", owner.get("processId"))
    if state.get("processId") is not None and not process_alive(state["processId"]):
        raise BridgeError("Bridge process has exited; use --start to recover and start SAP GUI with its bridge.")
    if state.get("stopped"):
        raise BridgeError("Bridge is stopped: " + state.get("error", "use --start to start a new bridge instance"))
    if time.time() * 1000 - state.get("heartbeatAt", 0) > freshness * 1000:
        raise BridgeError("Bridge heartbeat is stale or a script is busy. Inspect SAP and pending files; do not restart or retry blindly.")
    return state


def process_alive(pid):
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        raise BridgeError("Cannot establish the old bridge process identity; preserve its control files.")
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def find_sapgui(explicit=None):
    if explicit:
        executable = explicit.expanduser().absolute()
        if executable.suffix == ".app":
            executable = executable / "Contents" / "MacOS" / "SAPGUI"
    elif sys.platform == "darwin":
        candidates = sorted(set(Path("/Applications").glob("SAPGUI*.app/Contents/MacOS/SAPGUI"))
                            | set(Path("/Applications/SAP Clients").glob("SAPGUI*/*.app/Contents/MacOS/SAPGUI")))
        if len(candidates) != 1:
            raise BridgeError("Expected one SAP GUI installation; pass --sapgui /absolute/path/to/SAPGUI.")
        executable = candidates[0]
    else:
        raise BridgeError("Pass --sapgui /absolute/path/to/native/launcher; live startup validation covers macOS.")
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise BridgeError("SAP GUI launcher is missing or not executable: " + str(executable))
    return executable


def start_bridge(root, executable, timeout, no_logon=False):
    if not root.exists() and not root.is_symlink():
        root.mkdir(mode=0o700, parents=True)
    private_directory(root)
    launch_lock = root / "launch.lock"
    try:
        launch_lock.mkdir(mode=0o700)
    except FileExistsError as error:
        raise BridgeError("Another startup owns launch.lock; inspect it before starting another client.") from error
    try:
        for name in ["client.lock", "request.json", "running.json"]:
            if (root / name).exists():
                raise BridgeError("Unresolved request/control file " + name + "; inspect its outcome before startup.")
        try:
            state = bridge_state(root)
        except BridgeError:
            state = None
        if state:
            return {"schema": "sap-gui-java-launch/v1", "ok": True, "phase": "bridge_ready",
                    "reused": True, "bridgeDir": str(root), "instanceId": state["instanceId"],
                    "processId": state.get("processId")}
        # A stale heartbeat is not evidence that a running script/client is dead.
        old_state = read_json(root / "bridge.json") if (root / "bridge.json").exists() else {}
        clean_stop = (old_state.get("stopped") is True and not old_state.get("error")
                      and old_state.get("activeRequest") is None and not (root / "server.lock").exists())
        owner = None
        for name in ["owner.json", "launcher.json", "bridge.json"]:
            if (root / name).exists():
                record = read_json(root / name)
                if record.get("processId") is not None:
                    owner = record
                    break
        if owner and process_alive(owner["processId"]) and not clean_stop:
            raise BridgeError("Previous SAP/bridge process is still alive; preserve that instance and inspect its state. "
                              "Use a separate --bridge-dir only if a new instance is intended.")
        if not owner and not clean_stop and any((root / name).exists() for name in ["server.lock", "bridge.json"]):
            raise BridgeError("Old bridge has no process identity. Preserve its files until its owner is confirmed stopped.")
        executable = find_sapgui(executable)
        source = Path(__file__).with_name("java-shell-bridge.js").read_text(encoding="utf-8")
        source = source.replace('var SAP_GUI_BRIDGE_DIRECTORY = "";',
                                "var SAP_GUI_BRIDGE_DIRECTORY = " + json.dumps(str(root)) + ";", 1)
        if owner or clean_stop:
            archive = root / ("previous-" + uuid.uuid4().hex)
            archive.mkdir(mode=0o700)
            for name in ["owner.json", "launcher.json", "bridge.json", "server.lock", "launcher.log", "bootstrap.js"]:
                if (root / name).exists():
                    (root / name).rename(archive / name)
        bootstrap = root / "bootstrap.js"
        bootstrap.write_text(source, encoding="utf-8")
        bootstrap.chmod(0o600)
        logfile = root / "launcher.log"
        # No shell, credentials, connection strings or manipulation of existing SAP processes.
        command = [str(executable), "-b", "-F", str(bootstrap)]
        if no_logon:
            command.insert(1, "-n")
        with logfile.open("w", encoding="utf-8") as log:
            logfile.chmod(0o600)
            child = subprocess.Popen(command, stdout=log, stderr=log, start_new_session=True)
        (root / "launcher.json").write_text(json.dumps({"schema": "sap-gui-java-launcher/v1",
            "processId": child.pid, "launchedAt": time.time() * 1000, "executable": str(executable)}), encoding="utf-8")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                state = bridge_state(root)
                return {"schema": "sap-gui-java-launch/v1", "ok": True, "phase": "bridge_ready",
                        "reused": False, "bridgeDir": str(root), "instanceId": state["instanceId"],
                        "processId": state.get("processId", child.pid),
                        "authentication": "Inspect sessions; use the client's normal login if none are authenticated"}
            except BridgeError:
                pass
            if child.poll() is not None:
                raise BridgeError("SAP launcher exited before the bridge became ready; inspect " + str(logfile))
            time.sleep(0.1)
        raise BridgeError("Startup timed out; SAP process " + str(child.pid) + " was preserved. Inspect "
                          + str(logfile) + " and bridge state before retrying.")
    finally:
        launch_lock.rmdir()


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
    command.add_argument("--start", action="store_true", help="Reuse an active bridge or launch SAP GUI with it automatically")
    parser.add_argument("--sapgui", type=Path, help="Native SAP GUI executable or macOS .app; only for --start")
    parser.add_argument("--no-logon", action="store_true", help="Omit the logon window for an isolated runtime probe; only for --start")
    args = parser.parse_args(argv)
    try:
        if not 0 < args.timeout <= 300:
            raise BridgeError("Use a timeout greater than 0 and at most 300 seconds.")
        if not args.start and (args.sapgui or args.no_logon):
            raise BridgeError("--sapgui and --no-logon require --start.")
        root = args.bridge_dir.expanduser().absolute()
        if args.start:
            response = start_bridge(root, args.sapgui, args.timeout, args.no_logon)
            print(json.dumps(response, ensure_ascii=False))
            return 0
        source = args.script.read_text(encoding="utf-8") if args.script else None
        operation = "run" if args.script else "stop" if args.stop else "status"
        response = submit(root, operation, source, args.timeout)
        print(json.dumps(response, ensure_ascii=False))
        return 0 if response["ok"] else 1
    except (BridgeError, OSError, ValueError) as error:
        print(json.dumps({"schema": "sap-gui-java-shell/v1", "ok": False, "transportError": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
