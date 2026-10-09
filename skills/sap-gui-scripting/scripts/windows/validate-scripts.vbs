Option Explicit
' Local fixtures only. Does not call GetObject or attach to SAP.
Dim files, source, code, config, app, session, result, message, cap
Set files = CreateObject("Scripting.FileSystemObject")
Set source = files.OpenTextFile(files.BuildPath(files.GetParentFolderName(WScript.ScriptFullName), "runtime.vbs"), 1)
code = source.ReadAll
source.Close
ExecuteGlobal code

Class FixtureInfo
    Public SystemName, Client, User, Transaction, Program, ScreenNumber
    Public ScriptingModeReadOnly, ScriptingModeRecordingDisabled
    Private Sub Class_Initialize
        SystemName = "TEST": Client = "001": User = "FIXTURE"
        Transaction = "SESSION_MANAGER": Program = "SAPLSMTR_NAVIGATION": ScreenNumber = "100"
        ScriptingModeReadOnly = False: ScriptingModeRecordingDisabled = False
    End Sub
End Class
Class FixtureWindow
    Public [Type]
    Private Sub Class_Initialize
        [Type] = "GuiMainWindow"
    End Sub
End Class
Class FixtureSession
    Public Id, Info, ActiveWindow, Busy, Actions
    Private Sub Class_Initialize
        Id = "/app/con[0]/ses[0]": Busy = False: Actions = 0
        Set Info = New FixtureInfo
        Set ActiveWindow = New FixtureWindow
    End Sub
    Public Sub StartTransaction(transaction)
        Actions = Actions + 1
        Err.Raise vbObjectError + 514, , "Unexpected fixture navigation."
    End Sub
End Class
Class FixtureConnection
    Public Children, DisabledByServer
    Private Sub Class_Initialize
        Set Children = CreateObject("Scripting.Dictionary")
        DisabledByServer = False
    End Sub
End Class
Class FixtureApp
    Public Children
    Private Sub Class_Initialize
        Dim connection
        Set Children = CreateObject("Scripting.Dictionary")
        Set connection = New FixtureConnection
        Children.Add CLng(0), connection
    End Sub
    Public Function FindById(id)
        Dim item
        For Each item In Children.Item(CLng(0)).Children.Items
            If item.Id = id Then Set FindById = item: Exit Function
        Next
        Err.Raise vbObjectError + 515, , "Session ID not found."
    End Function
End Class
Sub Assert(condition, description)
    If Not condition Then WScript.StdErr.WriteLine "FAIL: " & description: WScript.Quit 1
End Sub
Function SmokeError()
    Dim observed
    On Error Resume Next
    Set observed = SapSmoke(app, config)
    SmokeError = Err.Description
    Err.Clear
    On Error GoTo 0
End Function
Function ConfigError()
    On Error Resume Next
    SapValidate config
    ConfigError = Err.Description
    Err.Clear
    On Error GoTo 0
End Function

Set config = SapMap()
config.Add "systemName", "TEST": config.Add "client", "001": config.Add "user", "FIXTURE"
config.Add "sessionId", "": config.Add "table", "VBAK": config.Add "execute", False: config.Add "maxRows", "10"
SapValidate config
For Each cap In Array("0", "101", "1.5", "invalid", "")
    config("maxRows") = cap
    Assert InStr(ConfigError(), "row cap") > 0, "Invalid cap must fail before attachment: " & cap
Next
config("maxRows") = "10"
config("user") = ""
Assert InStr(ConfigError(), "Specify") > 0, "Missing identity"
config("user") = "FIXTURE"
config("table") = "VBAK;OTHER"
Assert InStr(ConfigError(), "table name") > 0, "Invalid table"
config("table") = "VBAK"
Assert SapJson("a" & Chr(34) & "\" & vbCrLf & ChrW(243)) = Chr(34) & "a\u0022\u005C\u000D\u000A\u00F3" & Chr(34), "JSON escaping"

Set app = New FixtureApp
Set session = New FixtureSession
app.Children.Item(CLng(0)).Children.Add CLng(0), session
Set result = SapInventory(app)
Assert UBound(result("errors")) = -1 And UBound(result("sessions")) = 0, "Inventory success"
Set result = SapSelect(app, config)
Assert result Is session, "Unique identity selection"
config("user") = "OTHER"
Assert InStr(SmokeError(), "found 0") > 0 And session.Actions = 0, "No identity match cannot navigate"
config("user") = "FIXTURE"
app.Children.Item(CLng(0)).Children.Add CLng(1), session
Assert InStr(SmokeError(), "found 2") > 0 And session.Actions = 0, "Ambiguous identity cannot navigate"
app.Children.Item(CLng(0)).Children.Remove CLng(1)
config("sessionId") = "/app/con[9]/ses[9]"
Assert InStr(SmokeError(), "found 0") > 0 And session.Actions = 0, "Wrong session ID cannot navigate"
config("sessionId") = ""
app.Children.Item(CLng(0)).DisabledByServer = True
Assert InStr(SmokeError(), "Incomplete inventory") > 0 And session.Actions = 0, "Server-disabled inventory cannot navigate"
app.Children.Item(CLng(0)).DisabledByServer = False
session.Busy = True
Assert InStr(SmokeError(), "Incomplete inventory") > 0 And session.Actions = 0, "Busy inventory cannot navigate"
session.Busy = False
session.Info.ScriptingModeReadOnly = True
Assert InStr(SmokeError(), "Read-only") > 0 And session.Actions = 0, "Read-only scripting cannot navigate"
session.Info.ScriptingModeReadOnly = False
session.ActiveWindow.Type = "GuiModalWindow"
Assert InStr(SmokeError(), "modal") > 0 And session.Actions = 0, "Unexpected modal cannot navigate"
session.ActiveWindow.Type = "GuiMainWindow"
session.Info.Transaction = "VA02"
Assert InStr(SmokeError(), "Easy Access") > 0 And session.Actions = 0, "Unrelated transaction cannot navigate"
WScript.Echo "PASS: Windows VBS configuration, JSON, inventory, exact selection and navigation stopping fixtures. No SAP attachment."
