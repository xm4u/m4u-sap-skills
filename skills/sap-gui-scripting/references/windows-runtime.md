# SAP GUI for Windows: COM execution

Use this adapter for the native Windows product, not SAP GUI for Java running on Windows. It uses Windows Script Host with VBScript and SAP's COM object model; no Node packages, Python, credentials, or new connection are required. Keep the complete `scripts/windows/` folder together: both entrypoints load `runtime.vbs` from their own directory.

## Readiness and inspection

Reuse an authenticated SAP session and confirm SAP GUI Scripting is installed. In SAP GUI Options, inspect **Accessibility & Scripting > Scripting > Enable scripting**. Server restrictions are the same `sapgui/user_scripting*` settings described in [Java setup](setup-and-runtime.md#client-and-server-readiness); transaction/table authorizations still apply. Diagnose restrictions without changing notification, registry, security, or server settings implicitly.

From the repository root, run:

```powershell
cscript.exe //nologo skills/sap-gui-scripting/scripts/windows/inspect-session.vbs
```

The script attaches using `GetObject("SAPGUI").GetScriptingEngine` and enumerates `Children.Count` / `Children.Item(index)`. JSON includes session ID, system, client, user, transaction, program, screen, scripting flags, window type, and inventory errors. Treat this identity-bearing output as local evidence. It reads metadata only. Busy or inaccessible sessions are reported as inventory errors; the action adapter refuses an incomplete inventory rather than choosing an arbitrary session.

## SE16/VBAK

Use the observed identity as named arguments; these example values are placeholders. Inspect the starting screen first: SAP Easy Access or SE16, without unrelated unsaved work or a modal. The scripts switch transactions and cannot detect every form of unsaved work.

```powershell
cscript.exe //nologo skills/sap-gui-scripting/scripts/windows/se16-table-smoke.vbs /system:YOUR_SYSTEM /client:YOUR_CLIENT /user:YOUR_USER /session:/app/con[0]/ses[0] /table:VBAK
```

`/session` is optional when the identity matches exactly one reachable session. It supplements identity; connection/session indices are not persistent identifiers. Quote an entire argument if it contains spaces. Default mode opens the selection screen without querying. For the requested bounded display:

```powershell
cscript.exe //nologo skills/sap-gui-scripting/scripts/windows/se16-table-smoke.vbs /system:YOUR_SYSTEM /client:YOUR_CLIENT /user:YOUR_USER /session:/app/con[0]/ses[0] /table:VBAK /execute:true /maxRows:10
```

`/execute` accepts only `true` or `false`; `/maxRows` defaults to 10 and must be an integer from 1 to 100. Identity, table syntax, and cap are checked before attachment. The runtime checks read-only scripting, modal state, the selection report `/1BCDWB/DBVBAK`, dynpro `1000`, and the maximum-hits control `wnd[0]/usr/txtMAX_SEL`. It reads the cap back before F8. Other screen variants need observed IDs/assertions, not removed checks.

Windows exposes `GuiSession.Busy`. This adapter polls it with a 30-second deadline after transitions, then reacquires controls and checks SAP errors and modality. A COM call itself can block longer than that deadline; this is not cancellation of a running SAP request. A row cap also does not bound total database work.

Success writes JSON to stdout, including the native window title and status text read through COM. A runtime error writes JSON to stderr and exits with code 1. `query_completed` proves a transition to a non-selection SE16 screen; verify table identity and hit count from the returned title and restriction message, with native visual inspection when needed. No desktop automation is required to run the scripts. Leave the requested results visible. Do not automatically restart a failed/uncertain workflow, dismiss unexpected dialogs, export rows, or log out.

## Compatibility and troubleshooting

| Symptom | Response |
| --- | --- |
| `GetObject` fails | Check that SAP GUI for Windows is running, scripting is installed, and the script runs in the same interactive Windows user context |
| `cscript`/VBScript blocked by policy or absent | Report the unavailable adapter; do not enable WSH or change security policy implicitly |
| Server-disabled, read-only, busy session, or incomplete inventory | Report effective restrictions/errors and inspect SAP before navigation |
| Multiple matches | Add the exact observed `/session` and repeat identity inspection |
| Wrong program or missing control | Inspect current transaction, report, dynpro and a Windows recording |
| PowerShell COM access fails with `0x80029C4A` / `TYPE_E_CANTLOADLIBRARY` | In the tested installation, `GetObject` attached but PowerShell's member binding failed; WSH VBScript worked. Use this WSH adapter; do not repair COM registration as an implicit step |
| Query exception or unexpected modal | Inspect the actual SAP screen/status; no blind retry or Enter |

The WSH adapter is the validated Windows path. Other COM hosts such as PowerShell or `win32com` need their own attachment/runtime validation. Windows VBScript (`.vbs`) and Java-client JavaScript (`.js`) use separate runtimes.
