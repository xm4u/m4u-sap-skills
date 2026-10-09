/* Load once in the authenticated SAP GUI for Java instance (Scripts > Scripting).
 * Agents then use java-shell.py through their ordinary shell.
 * Local file IPC, not an SAP external API. No connection, login or navigation.
 */
var SAP_GUI_BRIDGE_DIRECTORY = ""; // Default: ~/scripts/sap-gui-shell-bridge
var SAP_GUI_SHELL_BRIDGE;

(function () {
    if (typeof application === "undefined" || typeof Java === "undefined") {
        throw new Error("Load inside SAP GUI for Java with Java interop available.");
    }
    // Closing the script editor removes its preset globals. Keep the host in this closure.
    var hostApplication = application;
    var interop = Java;
    var Files = Java.type("java.nio.file.Files");
    var Paths = Java.type("java.nio.file.Paths");
    var Options = Java.type("java.nio.file.StandardCopyOption");
    var UTF8 = Java.type("java.nio.charset.StandardCharsets").UTF_8;
    var JString = Java.type("java.lang.String");
    var System = Java.type("java.lang.System");
    var Timer = Java.type("java.util.Timer");
    var TimerTask = Java.type("java.util.TimerTask");
    var UUID = Java.type("java.util.UUID");
    var PosixPermissions = Java.type("java.nio.file.attribute.PosixFilePermissions");
    var root = Paths.get(SAP_GUI_BRIDGE_DIRECTORY ||
        String(System.getProperty("user.home")) + "/scripts/sap-gui-shell-bridge");
    if (Files.isSymbolicLink(root)) {
        throw new Error("Bridge directory must not be a symlink.");
    }
    Files.createDirectories(root);
    try {
        Files.setPosixFilePermissions(root, PosixPermissions.fromString("rwx------"));
    } catch (permissionsError) {
        throw new Error("This file bridge requires a private POSIX directory: " + permissionsError);
    }
    var serverLock = root.resolve("server.lock");
    // Exclusive creation prevents two SAP instances consuming the same requests.
    Files.createFile(serverLock);
    var instanceId = String(UUID.randomUUID());
    var requestPath = root.resolve("request.json");
    var runningPath = root.resolve("running.json");
    var started = Date.now();
    var stopped = false;
    var activeRequest = null;
    var timer;

    function writeJSON(filename, value) {
        var destination = root.resolve(filename);
        var temporary = root.resolve(filename + ".tmp");
        Files.write(temporary, new JString(JSON.stringify(value)).getBytes(UTF8));
        Files.move(temporary, destination, interop.to([Options.ATOMIC_MOVE, Options.REPLACE_EXISTING],
            "java.nio.file.CopyOption[]"));
    }
    function state() {
        return {schema: "sap-gui-java-bridge/v1", instanceId: instanceId,
            startedAt: started, heartbeatAt: Date.now(), stopped: stopped,
            activeRequest: activeRequest,
            majorVersion: Number(hostApplication.majorVersion),
            minorVersion: Number(hostApplication.minorVersion),
            revision: Number(hostApplication.revision)};
    }
    function stop() {
        stopped = true;
        timer.cancel();
        writeJSON("bridge.json", state());
        Files.deleteIfExists(serverLock);
    }
    function tick() {
        if (stopped) { return; }
        try {
            writeJSON("bridge.json", state());
            if (!Files.exists(requestPath)) { return; }
            // Claim before executing: a request is never automatically replayed.
            Files.move(requestPath, runningPath, interop.to([Options.ATOMIC_MOVE],
                "java.nio.file.CopyOption[]"));
            if (Number(Files.size(runningPath)) > 1048576) {
                throw new Error("Request exceeds 1 MiB; inspect running.json.");
            }
            var request = JSON.parse(String(new JString(Files.readAllBytes(runningPath), UTF8)));
            if (!/^[a-f0-9]{32}$/.test(request.requestId) || request.instanceId !== instanceId) {
                throw new Error("Invalid request identity; inspect running.json.");
            }
            activeRequest = request.requestId;
            writeJSON("bridge.json", state());
            var response = {schema: "sap-gui-java-shell/v1", instanceId: instanceId,
                requestId: request.requestId, ok: false};
            var shouldStop = false;
            try {
                if (request.operation === "status") {
                    response.result = state();
                } else if (request.operation === "stop") {
                    response.result = {stopped: true};
                    shouldStop = true;
                } else if (request.operation === "run" && typeof request.source === "string") {
                    // SAP host objects remain in this interpreter's scope. No Node runtime.
                    var value = (function (application, source) {
                        return eval(source);
                    }(hostApplication, request.source));
                    if (typeof value === "string") {
                        try { value = JSON.parse(value); } catch (notJSON) { /* Keep text. */ }
                    }
                    response.result = typeof value === "undefined" ? null : value;
                    // Convert non-serializable host results to an explicit script failure.
                    JSON.stringify(response);
                } else {
                    throw new Error("Unsupported bridge operation.");
                }
                response.ok = true;
            } catch (scriptError) {
                response.ok = false;
                response.error = String(scriptError);
                delete response.result;
            }
            writeJSON("response-" + request.requestId + ".json", response);
            Files.deleteIfExists(runningPath);
            activeRequest = null;
            if (shouldStop) { stop(); } else { writeJSON("bridge.json", state()); }
        } catch (transportError) {
            // Keep the claimed request for diagnosis; never repeat an uncertain action.
            stopped = true;
            timer.cancel();
            writeJSON("bridge.json", {schema: "sap-gui-java-bridge/v1", instanceId: instanceId,
                heartbeatAt: Date.now(), stopped: true, error: String(transportError),
                activeRequest: activeRequest});
        }
    }
    try {
        if (Files.exists(requestPath) || Files.exists(runningPath)) {
            throw new Error("Pending request exists; inspect it before restarting the bridge.");
        }
        timer = new Timer("SAP GUI local shell bridge", true);
        var Task = Java.extend(TimerTask, {run: tick});
        SAP_GUI_SHELL_BRIDGE = {timer: timer, directory: String(root), instanceId: instanceId};
        writeJSON("bridge.json", state());
        timer.schedule(new Task(), 250, 250);
    } catch (startupError) {
        if (timer) { timer.cancel(); }
        Files.deleteIfExists(serverLock);
        throw startupError;
    }
    return JSON.stringify({schema: "sap-gui-java-bridge-start/v1", directory: String(root),
        instanceId: instanceId, started: true});
}());
