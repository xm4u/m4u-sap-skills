Option Explicit
' Named arguments keep target identity outside reusable files. Default: selection only.
Dim files, source, code, config, execute, sapAuto, app, result, message
Set files = CreateObject("Scripting.FileSystemObject")
Set source = files.OpenTextFile(files.BuildPath(files.GetParentFolderName(WScript.ScriptFullName), "runtime.vbs"), 1)
code = source.ReadAll
source.Close
ExecuteGlobal code
Function Argument(name, fallback)
    If WScript.Arguments.Named.Exists(name) Then
        Argument = CStr(WScript.Arguments.Named.Item(name))
    Else
        Argument = fallback
    End If
End Function
On Error Resume Next
execute = Argument("execute", "false")
If execute <> "true" And execute <> "false" Then SapFail "Use /execute:true or /execute:false."
If Err.Number <> 0 Then
    message = Err.Description
    Err.Clear
    SapReportError "configuration", message
End If
Set config = SapMap()
config.Add "systemName", Argument("system", "")
config.Add "client", Argument("client", "")
config.Add "user", Argument("user", "")
config.Add "sessionId", Argument("session", "")
config.Add "table", Argument("table", "VBAK")
config.Add "execute", execute = "true"
config.Add "maxRows", Argument("maxRows", "10")
SapValidate config
If Err.Number <> 0 Then
    message = Err.Description
    Err.Clear
    SapReportError "configuration", message
End If
Set sapAuto = GetObject("SAPGUI")
If Err.Number = 0 Then Set app = sapAuto.GetScriptingEngine
If Err.Number = 0 Then Set result = SapSmoke(app, config)
If Err.Number <> 0 Then
    message = Err.Description
    Err.Clear
    SapReportError "se16", message
End If
On Error GoTo 0
WScript.Echo SapJson(result)
