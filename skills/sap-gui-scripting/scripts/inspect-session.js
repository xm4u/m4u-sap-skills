/* Submit through java-shell.py --script, or load in SAP GUI's scripting editor.
 * Reads session metadata only. Does not navigate, log in, or export table data.
 */
(function () {
    if (typeof application === "undefined") {
        throw new Error("Run this script in SAP GUI for Java, not Node.js or a browser.");
    }
    var result = {schema: "sap-gui-java-inspection/v1", sessions: [], errors: []};
    var connections = application.children;
    for (var c = 0; c < connections.length; c++) {
        try {
            var connection = connections.elementAt(c);
            var sessions = connection.children;
            for (var s = 0; s < sessions.length; s++) {
                try {
                    var candidate = sessions.elementAt(s);
                    var info = candidate.info;
                    result.sessions.push({
                        connectionId: String(connection.id),
                        sessionId: String(candidate.id),
                        systemName: String(info.systemName),
                        client: String(info.client),
                        user: String(info.user),
                        transaction: String(info.transaction),
                        program: String(info.program),
                        screenNumber: String(info.screenNumber),
                        scriptingModeReadOnly: Boolean(info.scriptingModeReadOnly),
                        scriptingModeRecordingDisabled: Boolean(info.scriptingModeRecordingDisabled)
                    });
                } catch (sessionError) {
                    result.errors.push({connectionIndex: c, sessionIndex: s, error: String(sessionError)});
                }
            }
        } catch (connectionError) {
            result.errors.push({connectionIndex: c, error: String(connectionError)});
        }
    }
    return JSON.stringify(result, null, 2);
}());
