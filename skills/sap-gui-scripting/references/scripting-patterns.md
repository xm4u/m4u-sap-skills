# Java scripting patterns

## Object model and Java syntax

The practical hierarchy is `application → connection → session → window → control`. SAP's general API documentation frequently shows Windows/VB syntax. Verify the Java implementation before copying methods or properties.

On Java 8.10 rev13, live-tested session enumeration uses lower-camel-case properties and `length`/`elementAt`:

```javascript
var connections = application.children;
for (var c = 0; c < connections.length; c++) {
    var connection = connections.elementAt(c);
    var sessions = connection.children;
    for (var s = 0; s < sessions.length; s++) {
        var candidate = sessions.elementAt(s);
        var info = candidate.info;
        // Match info.systemName, info.client and info.user here.
    }
}
```

Do not substitute `Children(0)`, `.Count`, `GetObject("SAPGUI")`, `win32com`, or `WScript`. Avoid assuming Node imports, DOM globals, timers, or modern JavaScript syntax are available. The bundled scripts use ES5-compatible syntax. `return JSON.stringify(result, null, 2)` at the end of an immediately invoked function produces visible editor output in the tested client.

## Recording and IDs

| Recording option | Reference shape | Portability |
| --- | --- | --- |
| Absolute ID | `application.findById("/app/con[0]/ses[0]/wnd[0]/usr/...")` | Connection/session indices must match at replay time |
| Relative ID | `window.findById("usr/...")` or `userarea.findById("...")` | Depends on the current window/area binding |
| Common SAP GUI ID | `session.findById("wnd[0]/usr/...")` | Fits an explicitly selected session and is useful for reusable procedures |

Different users can choose the same format without collisions. Changing the recording preference does not transform existing files. For reusable automation, normalize recorded actions to a verified session object plus session-relative paths. Do not hardcode connection indices as identity.

Use the Java client's recorder to obtain exact field, toolbar, tab, grid, and table IDs on the target system. An ID from another system, screen variant, or transaction version is only a hypothesis until observed. Field prefixes such as `ctxt`, `txt`, `chk`, `rad`, and `btn` are useful hints, not an exhaustive ID grammar.

## Navigation and assertions

Before switching transactions, verify the system/client/user, active window type, current transaction, and whether work is in progress. Recheck identity when replaying a local file: a session ID alone is insufficient if connections have been reopened.

`session.startTransaction("SE16")` is available in the inspected Java runtime. `session.findById("wnd[0]").sendVKey(0)` sends Enter; `sendVKey(8)` sends F8. Discover other shortcuts in the installed API/recorder instead of copying an unverified virtual-key table.

After a round trip, read `session.info.transaction`, `program`, `screenNumber` and the status bar's `messageType`/`text`. Check the expected controls and values. Handle `E` and `A` as failures; interpret warnings/information in context rather than accepting them automatically. A lack of an error message is insufficient to prove the intended screen or data appeared.

The inspected Java session wrapper does not expose Windows' `Busy` property. Do not use `session.busy` as a universal Java wait condition. Let recorded synchronous actions complete, use expected-screen assertions at transitions, and let an external desktop orchestrator observe changes with a bounded timeout. Tight polling or sleeping on the UI thread can prevent progress.

## Popups, tables, and reuse

- Check `session.activeWindow.type`; stop or handle an expected modal by its observed title, fields, and action. `wnd[1]` is a conventional path, not a guarantee that a popup should be confirmed.
- Reacquire controls after navigation, tab changes, table scrolling, or refresh. The session can remain valid while old screen-control references become stale.
- Distinguish a classic `GuiTableControl` from an ALV/grid shell by the actual `type`. Verify Java methods and column identifiers before extracting values; never infer the control API from its visual appearance alone.
- Limit result size for a smoke test. Do not execute an unrestricted table read or increase output limits just to make an assertion pass. A result limit constrains displayed rows; it is not a guaranteed database scan/time limit.
- Retry only a demonstrably repeatable read/inspection after rechecking the screen. After a business write or uncertain outcome, inspect the result before deciding whether another action is safe.
