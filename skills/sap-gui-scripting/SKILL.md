---
name: sap-gui-scripting
description: Automate SAP GUI from a shell using the Java local script bridge or Windows COM/VBScript. Use for session inspection, transaction navigation, ABAP editor workflows and GUI tests. SAP GUI for HTML and Fiori need another adapter.
---

# SAP GUI scripting and testing

Identify the actual SAP client before choosing an adapter:

- **SAP GUI for Java on macOS**: prefer [Java shell execution](references/java-shell-runtime.md). Run `python3 scripts/java-shell.py --start`: it reuses a ready bridge or starts SAP GUI with the bridge automatically, including recovery after a confirmed process exit. Then submit `scripts/inspect-session.js` with `--script`. Do not require manual script loading for this startup workflow. An existing unbridged client cannot be attached through the launcher; preserve it and use the new instance's normal login. Java on Linux requires separate validation; other Java environments retain the built-in editor workflow.
- **SAP GUI for Windows**: run `scripts/windows/*.vbs` with `cscript.exe //nologo`. These scripts attach to an existing authenticated session through COM. Read [Windows setup and execution](references/windows-runtime.md).

A skill supplies instructions and scripts; it does not install SAP or authenticate a user. Node/browser JavaScript does not provide either client's SAP host objects. With the Java bridge, Python transports files while SAP's engine executes the script. Verify screens and requested outcomes through scripting assertions; add native desktop inspection when available. A computer-use tool is not required for an already running bridge or Windows COM.

## Workflow

1. Establish the requested outcome and whether it needs session inspection, navigation, reading business data, or a business change. Use the user's existing authorization; do not request it again for actions already authorized. Creating the skill itself does not authorize running arbitrary SAP transactions.
2. Read the matching setup guide. Identify the client/version, open session, client-side scripting setting, and effective server restrictions. Reuse an authenticated session rather than requesting credentials.
3. Run the adapter's inspection script yourself when shell access is available. Do not ask the user to replay it or paste JSON if the Java bridge or Windows COM is ready. Read its inventory and errors. Select by system, mandant/client, user, and, when necessary, an explicitly observed session ID. Do not select the first child by default.
4. Read [Java scripting patterns](references/scripting-patterns.md) or [Windows runtime](references/windows-runtime.md) when adapting automation. Use the target client's recordings and observed control IDs. Separate session selection from paths rooted at the selected session.
5. For tests, read [testing and evidence](references/testing.md). Define observable assertions before running the workflow; verify the resulting screen, messages, and requested data after each significant transition.
6. Report the observed outcome, files produced, and remaining limitations. Distinguish local fixture validation, successful scripting execution, screen navigation, and actual data retrieval.

## Task routing

| Task | Resource |
| --- | --- |
| Java: automatic startup, shell scripts, JSON results and restart recovery | [Java shell execution](references/java-shell-runtime.md); [client/launcher](scripts/java-shell.py); [macOS shortcut](scripts/start-sapgui.command) |
| Java: enable/check scripting, load a file, handle local paths | [Setup and execution](references/setup-and-runtime.md) |
| Windows: COM attachment, WSH commands, settings, troubleshooting | [Windows setup and execution](references/windows-runtime.md) |
| Inspect sessions and effective scripting modes | Java [inspect-session.js](scripts/inspect-session.js); Windows [inspect-session.vbs](scripts/windows/inspect-session.vbs) |
| Choose an ID format, adapt a recording, navigate, handle tables or popups | [Scripting patterns](references/scripting-patterns.md) |
| Assert screens, reproduce a failure, build a regression case | [Testing and evidence](references/testing.md) |
| Test SE16/VBAK with an explicit target | [SE16 example and live baselines](references/se16-example.md); Java [script](scripts/se16-table-smoke.js); Windows [script](scripts/windows/se16-table-smoke.vbs) |
| Verify API availability or distinguish official documentation from upstream examples | [Sources and compatibility](references/sources.md) |

## Execution boundaries

- Preserve unrelated sessions and unsaved work. Transaction switches, including `/n` and `startTransaction`, can abandon the current screen. Inspect the starting state before navigating; the bundled SE16 example requires SAP Easy Access or SE16.
- Do not change profile parameters, roles, trust settings, notification options, or connection configuration as an implicit fix. Diagnose effective restrictions and apply only changes covered by the user's request.
- Resolve unexpected modal windows explicitly. Do not blindly press Enter, confirm multiple logon dialogs, or retry save/post/delete actions.
- Java shell timeouts do not cancel SAP actions. Inspect the matching response and current state before recovering a lock or retrying; the native `-f`/`-F` launcher is not attachment to an existing authenticated instance.
- Keep credentials, customer identifiers, hostnames, and captured business rows out of reusable skill files. Configure local script copies; redact evidence before sharing it.
- SAP GUI for Java also runs on Windows; choose by client product, not OS alone. Its `application`, `children.length` and `elementAt` differ from Windows COM's `GetObject("SAPGUI")`, `Children.Count` and `Children.Item`. Do not load the Windows scripts into the Java editor.
