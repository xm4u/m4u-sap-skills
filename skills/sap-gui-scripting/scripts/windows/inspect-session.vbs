Option Explicit
' cscript.exe //nologo inspect-session.vbs
Dim files, source, code, sapAuto, app, result, message
Set files = CreateObject("Scripting.FileSystemObject")
Set source = files.OpenTextFile(files.BuildPath(files.GetParentFolderName(WScript.ScriptFullName), "runtime.vbs"), 1)
code = source.ReadAll
source.Close
ExecuteGlobal code
On Error Resume Next
Set sapAuto = GetObject("SAPGUI")
If Err.Number = 0 Then Set app = sapAuto.GetScriptingEngine
If Err.Number = 0 Then Set result = SapInventory(app)
If Err.Number <> 0 Then
    message = Err.Description
    Err.Clear
    SapReportError "inspection", message
End If
On Error GoTo 0
WScript.Echo SapJson(result)
If UBound(result("errors")) >= 0 Then WScript.Quit 1
