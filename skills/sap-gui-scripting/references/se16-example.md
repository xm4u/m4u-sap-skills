# SE16 table display smoke test

## Scope

The Java [script](../scripts/se16-table-smoke.js) and Windows [COM script](../scripts/windows/se16-table-smoke.vbs) select an authenticated session, enter SE16, and open the requested table's selection screen. The table defaults to `VBAK`. Optional execute mode sets a small result limit and displays the list; it does not create, save, update, or delete records. For Windows commands and arguments, read [Windows execution](windows-runtime.md#se16vbak). The local-copy configuration below applies to Java.

The example targets the observed classic SE16 screen: selection report `/1BCDWB/DB` plus the table name, dynpro `1000`, and maximum-hits field `txtMAX_SEL`. Other table names, namespace conventions, screen variants, or SAP releases may need an adapted report assertion or control IDs. Do not remove a failed assertion merely to force execution; inspect the actual screen.

## Configure a local copy

First replay `inspect-session.js`. Copy the action script into a local working directory outside the repository and configure its first variables with the observed target:

```javascript
var SAP_GUI_TARGET = {
    systemName: "YOUR_SYSTEM",
    client: "YOUR_CLIENT",
    user: "YOUR_USER",
    sessionId: "" // Set the observed ID if multiple sessions match.
};
var SAP_GUI_TABLE = "VBAK";
var SAP_GUI_EXECUTE = false;
var SAP_GUI_MAX_ROWS = 10;
```

The shipped script leaves target identity empty intentionally and refuses to navigate until configured. Keep system/client/user as strings. An absolute session ID supplements identity checks; it is not a persistent user identifier.

Start at SAP Easy Access (`SESSION_MANAGER`) or SE16 with no unrelated unsaved work. Replay from **Scripts > Scripting**. With execute disabled, expect a returned `phase: "selection"`, transaction `SE16`, report `/1BCDWB/DBVBAK`, and screen `1000`; verify the visible VBAK selection screen.

For a user-requested data display, set `SAP_GUI_EXECUTE = true` in the local copy. The script validates the row limit as an integer from 1 to 100, sets `wnd[0]/usr/txtMAX_SEL`, checks it was applied, and sends F8 once. The row cap limits results, not the total database work. A correctness/regression case should also use a known key or filter adapted from a recording rather than relying on whichever first rows appear.

## Expected evidence

- Exactly one target session matched before navigation.
- Scripting was not effectively read-only and the active window was not modal.
- The table selection field was `wnd[0]/usr/ctxtDATABROWSE-TABLENAME`.
- After Enter, transaction/report/dynpro matched the selection screen.
- Before execution, the configured maximum was read back from `txtMAX_SEL`.
- With execution enabled, the action reached a non-selection SE16 screen without an error/modal. The returned phase is `query_completed`; inspect the native list separately to prove table identity and rows.

Replay in the editor when JSON output is needed. Scripts in configured directories can also be launched directly from the **Scripts** menu; in the tested client this showed a completion dialog instead of the editor's returned JSON. A completion dialog does not replace checking the resulting session screen.

## Java live baseline: 2026-10-09

Passed on **macOS, SAP GUI for Java 8.10 rev13**, using an existing authenticated session. Target identifiers and business rows are omitted from this repository.

| Check | Observed result |
| --- | --- |
| Session inspection | One reachable session; no inventory errors; read-only and recording-disabled flags both false |
| SE16 entry and VBAK selection | Script returned `SE16`, `/1BCDWB/DBVBAK`, screen `1000`; selection title confirmed in the native UI |
| Maximum-hits control | Control inspection confirmed `wnd[0]/usr/txtMAX_SEL` |
| Bounded query | Script configured with execute enabled and row cap 10 completed successfully |
| Visible results | Native list title identified VBAK with **10 hits**; status confirmed selection restricted to 10 hits |
| Final result program | Native session information showed `SAPLSLVC_FULLSCREEN` |
| Finish state | VBAK result list left visible; no record changes, export, or logout performed |

This proves session access, navigation, and a bounded data display on the tested client/system. It does not establish row-content correctness, performance thresholds, unattended attachment, write workflows, or Windows/Linux compatibility.

## Windows live baseline: 2026-10-09

Passed on **Windows, native SAP GUI for Windows 8.10 (64-bit)** using an existing authenticated session. Installed `saplogon.exe` file version: `8100.1.1.1161`; `sapfewse.ocx`: `8100.1.1.257`. This is a separate run from the macOS baseline. Target identifiers and business rows are omitted.

| Check | Observed result |
| --- | --- |
| Initial state | SAP Easy Access, transaction `SESSION_MANAGER`; no modal |
| External COM inspection | WSH VBScript inventory returned one session, no errors; read-only and recording-disabled flags false |
| Navigation without execution | Windows script returned phase `selection`, `SE16`, `/1BCDWB/DBVBAK`, screen `1000`; native title confirmed VBAK selection |
| Bounded query | Windows script with `/execute:true /maxRows:10` read back `txtMAX_SEL` and returned phase `query_completed` |
| Result program/dynpro | `SAPLSLVC_FULLSCREEN`, screen `500`, transaction `SE16` |
| Visible results | Native title `Data Browser: Tabla VBAK 10 aciertos`; ten displayed rows; status `La selección se ha restringido a 10 acierto(s)` |
| Finish state | VBAK result list left visible; no record changes, export, or logout |

The final VBScript adapter was rerun successfully on request. It returned `query_completed`, cap `10`, `SE16`, `SAPLSLVC_FULLSCREEN`, dynpro `500`, title `Data Browser: Tabla VBAK         10 aciertos`, and status `La selección se ha restringido a 10 acierto(s)` directly through COM. Desktop automation was used for the initial visual verification; it is not part of the VBS execution path.

PowerShell 7.6.5 and Windows PowerShell 5.1 attached to the ROT object but failed accessing the scripting engine with `TYPE_E_CANTLOADLIBRARY`. The shipped WSH VBScript adapter succeeded without changing registration or settings. This validates the shipped Windows path on this installation, not every COM host or system/screen variant. Row-content correctness, deterministic business fixtures, performance, write workflows, and other releases remain untested.
