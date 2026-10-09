/* Run in SAP GUI for Java via java-shell.py or the editor. Configure a COPY below.
 * Opens SE16 and the table selection screen, optionally executing a bounded read.
 * Does not save or change records.
 * A read-only business transaction still requires navigation-capable scripting.
 */
var SAP_GUI_TARGET = {systemName: "", client: "", user: "", sessionId: ""};
var SAP_GUI_TABLE = "VBAK";
var SAP_GUI_EXECUTE = false;
var SAP_GUI_MAX_ROWS = 10;

(function () {
    if (typeof application === "undefined") {
        throw new Error("Run inside SAP GUI for Java.");
    }
    var target = SAP_GUI_TARGET;
    if (!target.systemName || !target.client || !target.user) {
        throw new Error("Configure systemName, client and user in a local copy first.");
    }
    if (!/^[A-Z0-9_\/]+$/.test(SAP_GUI_TABLE)) {
        throw new Error("Invalid table name.");
    }
    if (SAP_GUI_EXECUTE !== true && SAP_GUI_EXECUTE !== false) {
        throw new Error("SAP_GUI_EXECUTE must be a boolean.");
    }
    if (typeof SAP_GUI_MAX_ROWS !== "number" || !isFinite(SAP_GUI_MAX_ROWS) ||
            SAP_GUI_MAX_ROWS < 1 || SAP_GUI_MAX_ROWS > 100 ||
            Math.floor(SAP_GUI_MAX_ROWS) !== SAP_GUI_MAX_ROWS) {
        throw new Error("Use an integer row cap between 1 and 100 for this smoke test.");
    }
    var matches = [];
    var connections = application.children;
    for (var c = 0; c < connections.length; c++) {
        var sessions = connections.elementAt(c).children;
        for (var s = 0; s < sessions.length; s++) {
            var candidate = sessions.elementAt(s);
            var info = candidate.info;
            if (String(info.systemName) === target.systemName &&
                    String(info.client) === target.client &&
                    String(info.user) === target.user &&
                    (!target.sessionId || String(candidate.id) === target.sessionId)) {
                matches.push(candidate);
            }
        }
    }
    if (matches.length !== 1) {
        throw new Error("Expected exactly one matching session; found " + matches.length + ".");
    }
    var selected = matches[0];
    if (selected.info.scriptingModeReadOnly) {
        throw new Error("Server-side read-only scripting blocks transaction navigation.");
    }
    if (String(selected.activeWindow.type) !== "GuiMainWindow") {
        throw new Error("Resolve the modal window before navigation.");
    }
    var transaction = String(selected.info.transaction);
    if (transaction !== "SESSION_MANAGER" && transaction !== "SE16") {
        throw new Error("Start from SAP Easy Access or SE16; current transaction: " + transaction);
    }
    selected.startTransaction("SE16");
    selected.findById("wnd[0]/usr/ctxtDATABROWSE-TABLENAME").text = SAP_GUI_TABLE;
    selected.findById("wnd[0]").sendVKey(0);
    var status = selected.findById("wnd[0]/sbar");
    if (String(status.messageType) === "E" || String(status.messageType) === "A") {
        throw new Error("SAP rejected the table: " + String(status.text));
    }
    if (String(selected.info.transaction) !== "SE16" ||
            String(selected.info.screenNumber) !== "1000" ||
            String(selected.activeWindow.type) !== "GuiMainWindow") {
        throw new Error("Expected the SE16 selection screen without a modal window.");
    }
    if (String(selected.info.program) !== "/1BCDWB/DB" + SAP_GUI_TABLE) {
        throw new Error("Unexpected selection program; verify the table and screen variant.");
    }
    if (SAP_GUI_EXECUTE) {
        var maximum = selected.findById("wnd[0]/usr/txtMAX_SEL");
        maximum.text = String(SAP_GUI_MAX_ROWS);
        if (Number(String(maximum.text)) !== SAP_GUI_MAX_ROWS) {
            throw new Error("The result limit was not applied; do not execute.");
        }
        selected.findById("wnd[0]").sendVKey(8);
        status = selected.findById("wnd[0]/sbar");
        if (String(status.messageType) === "E" || String(status.messageType) === "A" ||
                String(selected.activeWindow.type) !== "GuiMainWindow" ||
                String(selected.info.transaction) !== "SE16" ||
                String(selected.info.screenNumber) === "1000") {
            throw new Error("Query did not reach a result screen; inspect SAP before retrying.");
        }
    }
    return JSON.stringify({
        schema: "sap-gui-java-se16/v1",
        phase: SAP_GUI_EXECUTE ? "query_completed" : "selection",
        table: SAP_GUI_TABLE,
        maxRows: SAP_GUI_EXECUTE ? SAP_GUI_MAX_ROWS : null,
        sessionId: String(selected.id),
        transaction: String(selected.info.transaction),
        program: String(selected.info.program),
        screenNumber: String(selected.info.screenNumber)
    }, null, 2);
}());
