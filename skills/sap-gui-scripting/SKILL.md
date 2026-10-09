---
name: sap-gui-scripting
description: Automate and test SAP GUI for Java sessions on macOS, Linux, and Windows using the client's built-in JavaScript scripting engine. Use for session inspection, recorded scripts, transaction navigation, SAP screen assertions, and GUI regression tests. Windows COM, VBScript, win32com, SAP GUI for HTML, and Fiori need a different execution adapter.
---

# SAP GUI for Java scripting and testing

Use JavaScript executed **inside SAP GUI for Java**. A skill supplies instructions and scripts; it does not install an external session connector. Use the available desktop automation tool to load/replay scripts and inspect results, or have the user replay them if desktop control is unavailable. Do not claim a terminal, Node.js, Python, or browser process has attached to SAP merely because it runs JavaScript.

## Workflow

1. Establish the requested outcome and whether it needs session inspection, navigation, reading business data, or a business change. Use the user's existing authorization; creating the skill itself does not authorize running arbitrary SAP transactions.
2. Read [setup and execution](references/setup-and-runtime.md). Identify the actual client and version, open session, client-side scripting setting, and effective server restrictions. Reuse an authenticated session rather than requesting credentials.
3. Run [inspect-session.js](scripts/inspect-session.js) inside SAP GUI when live inspection is available. Read its returned session inventory and errors. Select by system, mandant/client, user, and, when necessary, an explicitly observed session ID. Do not select the first child by default.
4. Read [scripting patterns](references/scripting-patterns.md) when creating or adapting automation. Use Java recordings and observed control IDs. Separate session selection from control paths rooted at the selected session.
5. For tests, read [testing and evidence](references/testing.md). Define observable assertions before running the workflow; verify the resulting screen, messages, and requested data after each significant transition.
6. Report the observed outcome, files produced, and remaining limitations. Distinguish local fixture validation, successful scripting execution, screen navigation, and actual data retrieval.

## Task routing

| Task | Resource |
| --- | --- |
| Enable/check scripting, load a file, handle local paths or platform differences | [Setup and execution](references/setup-and-runtime.md) |
| Inspect connections, sessions, transactions, and effective scripting modes | [inspect-session.js](scripts/inspect-session.js) |
| Choose an ID format, adapt a recording, navigate, handle tables or popups | [Scripting patterns](references/scripting-patterns.md) |
| Assert screens, reproduce a failure, build a regression case | [Testing and evidence](references/testing.md) |
| Test SE16 and a table such as VBAK with an explicit target | [SE16 example](references/se16-example.md) and [se16-table-smoke.js](scripts/se16-table-smoke.js) |
| Verify API availability or distinguish official documentation from upstream examples | [Sources and compatibility](references/sources.md) |

## Execution boundaries

- Preserve unrelated sessions and unsaved work. Transaction switches, including `/n` and `startTransaction`, can abandon the current screen. Inspect the starting state before navigating; the bundled SE16 example requires SAP Easy Access or SE16.
- Do not change profile parameters, roles, trust settings, notification options, or connection configuration as an implicit fix. Diagnose effective restrictions and apply only changes covered by the user's request.
- Resolve unexpected modal windows explicitly. Do not blindly press Enter, confirm multiple logon dialogs, or retry save/post/delete actions.
- Keep credentials, customer identifiers, hostnames, and captured business rows out of reusable skill files. Configure local script copies; redact evidence before sharing it.
- SAP GUI for Java also runs on Windows. That does not turn it into SAP GUI for Windows or provide COM. Share a procedure across platforms only after checking the target client's methods and controls.
