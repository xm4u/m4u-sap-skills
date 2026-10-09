# Setup and execution

This page covers SAP GUI for Java's editor and client setup. For agents with shell access, start with [Java shell execution](java-shell-runtime.md): `java-shell.py --start` loads the bridge automatically at startup; scripts and JSON results are then exchanged through shell commands. For native SAP GUI for Windows, use [Windows COM setup](windows-runtime.md).

## Identify the runtime

Confirm that the application is **SAP GUI for Java**, its version/revision, and the target session's system, client, and user. macOS, Linux, and Windows are supported Java client platforms; SAP GUI for Windows is a separate product.

The supported starting path for this skill is the built-in JavaScript engine. Use the client's **Scripts > Scripting** window. On a localized client the replay button can have a surprising translation: Spanish 8.10 rev13 labels it **Devolución**. **Grabar** in the Scripts controls means record, not replay; the File menu's save-script command is separate.

An ordinary JavaScript runtime does not supply `application`, `session`, `window`, or `userarea`. These are SAP host objects determined by the script context. The bundled scripts use `application` and select a session explicitly so they also work in a global scripting window.

Use the bundled [local file bridge and launcher](java-shell-runtime.md) for shell control. It is a repository-provided transport around the built-in engine, not a native SAP external attachment API. `java-shell.py --start` uses `-F` to load it in a new process when no ready bridge exists; it does not see the user's sessions in another process. Do not invent an AppleScript dictionary, socket endpoint, REST API, or COM bridge. Desktop loading is an optional fallback for retaining an already-open unbridged instance.

## Client and server readiness

In **Preferences/Options > Web AS ABAP > Scripting**, confirm **On**. Notification checkboxes concern external script access/connection attempts; keeping them enabled is compatible with this workflow. A recording-ID choice controls newly recorded code and is not a user identity or permission setting.

On the ABAP application server, `sapgui/user_scripting` enables scripting. Further effective restrictions can depend on `sapgui/user_scripting_per_user`, `sapgui/user_scripting_set_readonly`, and `sapgui/user_scripting_disable_recording`. Where per-user authorization applies, check `S_SCR`; normal transaction and table authorizations still apply. Inspect/ask the administrator for the actual effective settings rather than prescribing one parameter combination for every environment.

`inspect-session.js` reports `scriptingModeReadOnly` and `scriptingModeRecordingDisabled` for reachable sessions. Read-only **scripting** can block navigation and field input even when the business operation would only display data. Recording disabled and scripting disabled are different conditions. A client checkbox is not proof of server permission, and a scripting-capable session is not proof of authorization to read a particular table.

## Load and replay

1. Inspect the current session screen. Keep the session and any settings dialog intact; use the Window menu to select the intended session if several windows are open.
2. Open **Scripts > Scripting**, then **File > Open Script** and select the `.js` file.
3. Verify the loaded filename and code. Replay it once and inspect the output pane. The bundled scripts return a JSON string from an immediately invoked function; the editor displays it under **RECEIVED**.
4. Read the returned result or exception, then inspect the SAP session window. **SENT** only proves the script was submitted; it is not completion. Allow a running request to finish before launching another one.

Use the configured script directories for menu discovery or select a file elsewhere with the file chooser. Check actual directory existence and write access before saving or exporting. Creating/loading a script does not require registering its directory in preferences. Keep local target configuration in a copy outside the repository.

Files in configured directories can be invoked directly from the **Scripts** menu. In the tested Java client this showed a completion dialog rather than the editor's returned JSON. Use the editor when collecting structured inspection output, and verify the native screen after either execution path.

With the file bridge already running, submit scripts through `java-shell.py --script` and read its JSON instead of reopening the editor. The bridge uses its own private IPC directory. SAP's `application.utils.openFile()` writes relative to the configured file-output directory; an absolute filename is not a way to select another output directory.

## Desktop tool caveats

Use an available native desktop automation tool according to its documentation, refreshing accessibility state after actions. Java Swing text controls may expose readable accessibility content without supporting value assignment. In that case use the tool's documented keyboard/paste operations, then verify the value; if the native file chooser fails to accept text, navigate through folders using its buttons and screenshot-based clicks.

Accessibility row clicks can also leave Swing lists unchanged. Inspect a screenshot and use the actual row position when supported. Do not repeat a no-op operation indefinitely, reuse stale element indices, or substitute shell-based mouse/keyboard injection for the desktop tool's supported actions.

## Troubleshooting

| Symptom | Next check |
| --- | --- |
| `application` is undefined | Execute in the SAP Java scripting window, not Node/browser/Python |
| No sessions or inventory errors | Authentication, connection state, client setting, effective server restrictions |
| More than one match | Add the observed session ID to the local target and verify its identity |
| Wrong/missing control | Current program/dynpro, modal window, recorder-derived ID and client support |
| SENT without RECEIVED | Request may still be running; inspect SAP and wait before submitting more actions |
| Empty output after a console-print helper | Return the result from the script; do not assume system console output appears in the editor |
| Authorization error in SE16 | Report the SAP message; do not alter roles or bypass checks |
