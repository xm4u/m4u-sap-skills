# Java execution from a shell

Use this adapter when an agent has shell access but no computer-use tool. The Python launcher starts SAP GUI with its local file bridge automatically, or reuses a ready bridge. Python coordinates files; SAP's built-in JavaScript engine executes the SAP calls. No network listener, stored credentials, Node packages, external SAP API, or accessibility permissions are needed.

## Automatic startup (preferred)

From the skill folder:

```sh
python3 scripts/java-shell.py --start
python3 scripts/java-shell.py --script scripts/inspect-session.js
```

`--start` returns `schema: sap-gui-java-launch/v1`, `phase: bridge_ready`, and `reused`. A ready bridge is reused without opening another process. Otherwise the launcher starts a new SAP GUI process with `-b -F bootstrap.js`, which loads the bridge automatically and opens SAP Logon. A macOS user can also double-click [start-sapgui.command](../scripts/start-sapgui.command) instead of opening the app directly.

**Bridge readiness is not authentication.** Inspect sessions next. If none are authenticated, use the new instance's normal connection/login flow; do not request passwords in chat. The launcher does not close, inject into, or transfer sessions from another open client. A client opened normally without a bridge remains separate. Do not ask a shell-only user to open the scripting editor when starting the new instance with `--start` is within the requested scope.

On macOS a single installation under `/Applications` or `/Applications/SAP Clients` is found automatically. With multiple installations or a different location, pass `--sapgui /absolute/path/to/SAPGUI.app` or its native executable. Java on Linux requires an explicit native launcher and separate validation.

After SAP exits, run the **same `--start` command**. The bridge records its process ID; the launcher checks process liveness, refuses unresolved requests, and archives old control files before starting a replacement. A recent heartbeat cannot mask an exited process. A stale heartbeat with a live process is preserved, since it can mean a running script. After a confirmed clean `--stop`, startup may also create a new bridge instance while preserving the old SAP client. Startup timeout preserves the new process and its private log for inspection rather than killing it or retrying automatically.

Use `--bridge-dir /absolute/private/path` consistently for an intentionally separate instance. `--no-logon` suppresses the logon window only for isolated runtime probes, not the normal user workflow.

## Optional bootstrap into an already-open authenticated instance

1. In the existing client, open **Scripts > Scripting > File > Open Script** and load [java-shell-bridge.js](../scripts/java-shell-bridge.js).
2. Replay once (Spanish 8.10 rev13: **Devolución**). Confirm `RECEIVED` with `started: true`. Default IPC directory: `~/scripts/sap-gui-shell-bridge`, mode `0700`.
3. Run the shell status command below. The script window may then be closed; the bridge remains in that client until stopped or the client exits.

A desktop-capable agent can perform this optional bootstrap. For a shell-only agent, prefer automatic startup above; manual loading is only a fallback when the user specifically needs to retain an already-open unbridged instance. If a bridge is active, do not replay it or ask the user to paste JSON. Loading the bridge does not authenticate, navigate, or modify SAP records.

This is a repository-provided adapter using Nashorn Java interop and standard Java file/timer APIs, **not an official SAP external attachment API**. Live validation covers macOS / Java 8.10 rev13. It requires Java interop, private POSIX files, atomic rename support, Python 3.8+, and effective SAP scripting permissions. Java on Linux needs separate validation. For the native Windows client use COM; this POSIX bridge is not the Java-on-Windows adapter.

To use another IPC directory, change `SAP_GUI_BRIDGE_DIRECTORY` in a local copy before loading and pass the same `--bridge-dir` to every shell command. Keep it private and local. Do not enable security permissions or change SAP trust/profile settings implicitly if startup fails.

## Commands

From the skill folder (use absolute paths when working elsewhere):

```sh
python3 scripts/java-shell.py --status
python3 scripts/java-shell.py --script scripts/inspect-session.js
```

Read the returned `result.sessions` and inventory errors. Match system, client, user, and an observed session ID before any navigation. A successful transport with zero sessions is not authenticated session access.

Configure a **local copy** of [se16-table-smoke.js](../scripts/se16-table-smoke.js) as described in the [SE16 guide](se16-example.md), then submit it:

```sh
python3 scripts/java-shell.py --script /absolute/local/path/se16-configured.js
```

Use the same command for task-specific scripts, including authorized SE38 development. Derive controls from recordings or an explicit control-tree inspection; keep identity checks, starting-state checks, modal handling and assertions in each script. Do not create/activate an ABAP program merely because the bridge is available. Follow the user's existing authorization; verification of system/client is not a demand for renewed permission.

Scripts use ES5-compatible syntax and the `application` host object. The final evaluated value becomes `result`; JSON strings returned by the bundled IIFEs are decoded automatically. Return only serializable values, not SAP/Java host objects. `printConsole()` goes to the SAP process's stderr and is not this shell command's result channel.

Responses are a single JSON object on stdout:

```json
{"schema":"sap-gui-java-shell/v1","instanceId":"...","requestId":"...","ok":true,"result":{"schema":"sap-gui-java-inspection/v1","sessions":[],"errors":[]}}
```

Exit codes: `0` script/transport completed, `1` script threw an error, `2` bridge/transport unavailable or uncertain. Inspect the underlying result and SAP assertions: exit `0` alone does not prove a business outcome. An inspection can return inventory errors even with transport `ok: true`.

## Serialization, timeout and recovery

Only one request runs at a time. The Python client acquires `client.lock`, sends an atomic request bound to `instanceId`, and checks the response ID. The bridge claims it as `running.json` **before** executing it and never automatically replays it. Script errors return `ok: false` and preserve the actual SAP state.

Default wait: 30 seconds; `--timeout` permits up to 300 seconds. **A timeout does not cancel a SAP action.** The client retains its lock and request ID. Read `client.lock/request.json`, `request.json`/`running.json`, any `response-<requestId>.json`, and the current SAP state. After an uncertain save/activate/post, determine the outcome before submitting anything else. Do not retry the whole script automatically.

The heartbeat pauses while a script runs. A stale heartbeat can mean a busy script, a closed client or a stopped bridge; it is not permission to start another bridge. When a timed-out request has actually completed, inspect its matching response and verify that `request.json` and `running.json` are absent before removing **only that request's** response and client-lock files.

After SAP GUI exits, `server.lock` can remain. `--start` recovers it automatically only with a recorded, exited owner and no unresolved request. Old files are preserved under `previous-<id>/`. Legacy bridges without process ownership cannot be recovered blindly; confirm the old process stopped before handling their files. Starting another bootstrap in an active directory is refused rather than replacing the consumer.

Stop the bridge without closing SAP or its sessions:

```sh
python3 scripts/java-shell.py --stop
```

The adapter accepts executable code from the same local OS user. Use trusted, task-authorized scripts; do not submit downloaded code or captured business content as executable input. IPC files can contain identifiers or business results; keep them local and redact any shared evidence. This transport is not an authorization sandbox.

## Why the native launcher is not existing-session attachment

The installed 8.10 rev13 launcher's `--help` documents `-f`/`-F` (asynchronous/synchronous script file) and `-s`/`-S` (script string). For example, on macOS:

```sh
"/Applications/SAPGUI 8.10rev13.app/Contents/MacOS/SAPGUI" --help
"/Applications/SAPGUI 8.10rev13.app/Contents/MacOS/SAPGUI" -n -b -F /absolute/path/script.js
```

In the tested client the second command started a **separate process with zero connections**, even while an authenticated instance was open. It must not be described as COM-style attachment. It can bootstrap a dedicated new instance when that is the requested workflow, but that instance still needs an authorized connection/login. Do not supply credentials or close an existing client to work around this difference.

## Validation

```sh
python3 scripts/validate-java-shell.py
pnpm exec node scripts/validate-scripts.cjs
```

The first command checks local protocol success/failure, mismatched responses, timeouts without replay, lock preservation, directory privacy, size bounds, startup reuse, live-owner refusal and exited-owner recovery. Neither command connects to SAP.

Live on **2026-10-09, macOS / SAP GUI for Java 8.10 rev13**: the bridge was loaded in an existing authenticated client; shell `--status` and the unmodified inspection script completed, reporting one session and no inventory errors. System/client/user were read through scripting, without manual JSON transfer or terminal accessibility permission. No navigation, record modification or business-row retrieval was performed for this transport validation. SE38 writes and Java on other platforms remain separate tests.

The automatic launcher was also tested in isolated clients with zero authenticated sessions: startup loaded the bridge without editor interaction, a second `--start` reused it, and after terminating that test client with `server.lock` retained the same command archived the old control files and started a new responding bridge. The executable macOS shortcut also passed startup with the normal logon window and an IPC path containing spaces. Clean stop/restart preserved the old test client. Authentication and SE38 development are separate checks.
