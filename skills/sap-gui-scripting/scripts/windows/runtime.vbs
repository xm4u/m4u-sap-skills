' Shared SAP GUI for Windows COM routines. No login, exports or record changes.
Function SapMap()
    Set SapMap = CreateObject("Scripting.Dictionary")
End Function

Function SapJson(value)
    Dim result, key, i, ch, code
    If IsObject(value) Then
        result = ""
        For Each key In value.Keys
            If Len(result) > 0 Then result = result & ","
            result = result & SapJson(CStr(key)) & ":" & SapJson(value.Item(key))
        Next
        SapJson = "{" & result & "}"
    ElseIf IsArray(value) Then
        result = ""
        For Each key In value
            If Len(result) > 0 Then result = result & ","
            result = result & SapJson(key)
        Next
        SapJson = "[" & result & "]"
    ElseIf IsNull(value) Or IsEmpty(value) Then
        SapJson = "null"
    ElseIf VarType(value) = vbBoolean Then
        If value Then SapJson = "true" Else SapJson = "false"
    ElseIf IsNumeric(value) And VarType(value) <> vbString Then
        SapJson = CStr(value)
    Else
        result = ""
        For i = 1 To Len(CStr(value))
            ch = Mid(CStr(value), i, 1)
            code = AscW(ch) And &HFFFF
            If code < 32 Or code > 126 Or ch = Chr(34) Or ch = "\" Then
                result = result & "\u" & Right("0000" & Hex(code), 4)
            Else
                result = result & ch
            End If
        Next
        SapJson = Chr(34) & result & Chr(34)
    End If
End Function

Sub SapFail(message)
    Err.Raise vbObjectError + 513, "sap-gui-windows", message
End Sub

Function SapMetadata(session)
    Dim info, item
    If session.Busy Then SapFail "Session busy; inspect again after completion."
    Set info = session.Info
    Set item = SapMap()
    item.Add "sessionId", CStr(session.Id)
    item.Add "systemName", CStr(info.SystemName)
    item.Add "client", CStr(info.Client)
    item.Add "user", CStr(info.User)
    item.Add "transaction", CStr(info.Transaction)
    item.Add "program", CStr(info.Program)
    item.Add "screenNumber", CStr(info.ScreenNumber)
    item.Add "scriptingModeReadOnly", CBool(info.ScriptingModeReadOnly)
    item.Add "scriptingModeRecordingDisabled", CBool(info.ScriptingModeRecordingDisabled)
    item.Add "windowType", CStr(session.ActiveWindow.Type)
    Set SapMetadata = item
End Function

Function SapInventory(app)
    Dim result, sessions, errors, c, s, connection, session, item, connectionCount, sessionCount
    Set result = SapMap()
    sessions = Array()
    errors = Array()
    On Error Resume Next
    connectionCount = app.Children.Count
    If Err.Number <> 0 Then
        Set item = SapMap()
        item.Add "message", Err.Description
        Err.Clear
        ReDim Preserve errors(UBound(errors) + 1)
        Set errors(UBound(errors)) = item
        connectionCount = 0
    End If
    For c = 0 To connectionCount - 1
        Set connection = app.Children.Item(CLng(c))
        If Err.Number = 0 Then
            If connection.DisabledByServer Then SapFail "Scripting disabled by server."
        End If
        If Err.Number = 0 Then
            sessionCount = connection.Children.Count
        End If
        If Err.Number <> 0 Then
            Set item = SapMap()
            item.Add "connectionIndex", c
            item.Add "message", Err.Description
            Err.Clear
            ReDim Preserve errors(UBound(errors) + 1)
            Set errors(UBound(errors)) = item
        Else
            For s = 0 To sessionCount - 1
                Set session = connection.Children.Item(CLng(s))
                If Err.Number = 0 Then Set item = SapMetadata(session)
                If Err.Number <> 0 Then
                    Set item = SapMap()
                    item.Add "connectionIndex", c
                    item.Add "sessionIndex", s
                    item.Add "message", Err.Description
                    Err.Clear
                    ReDim Preserve errors(UBound(errors) + 1)
                    Set errors(UBound(errors)) = item
                Else
                    ReDim Preserve sessions(UBound(sessions) + 1)
                    Set sessions(UBound(sessions)) = item
                End If
            Next
        End If
    Next
    On Error GoTo 0
    result.Add "schema", "sap-gui-windows-inspection/v1"
    result.Add "sessions", sessions
    result.Add "errors", errors
    Set SapInventory = result
End Function

Function SapSelect(app, config)
    Dim inventory, item, matches, sessionId
    Set inventory = SapInventory(app)
    If UBound(inventory("errors")) >= 0 Then SapFail "Incomplete inventory; inspect errors before navigation."
    matches = 0
    For Each item In inventory("sessions")
        If item("systemName") = config("systemName") And item("client") = config("client") And item("user") = config("user") Then
            If config("sessionId") = "" Or item("sessionId") = config("sessionId") Then
                matches = matches + 1
                sessionId = item("sessionId")
            End If
        End If
    Next
    If matches <> 1 Then SapFail "Expected exactly one matching session; found " & matches & "."
    Set SapSelect = app.FindById(sessionId)
End Function

Sub SapWait(session)
    Dim started
    started = Now
    Do While session.Busy
        If DateDiff("s", started, Now) >= 30 Then SapFail "SAP remains busy; inspect before retrying."
        WScript.Sleep 100
    Loop
End Sub

Sub SapScreen(session)
    Dim status
    If session.ActiveWindow.Type <> "GuiMainWindow" Then SapFail "Resolve the modal window before continuing."
    Set status = session.FindById("wnd[0]/sbar")
    If status.MessageType = "E" Or status.MessageType = "A" Then SapFail "SAP rejected the action: " & status.Text
End Sub

Sub SapValidate(config)
    Dim pattern, cap
    If config("systemName") = "" Or config("client") = "" Or config("user") = "" Then SapFail "Specify /system, /client and /user from inspection."
    Set pattern = New RegExp
    pattern.Pattern = "^[A-Z0-9_/]+$"
    If Not pattern.Test(config("table")) Then SapFail "Invalid table name."
    If VarType(config("execute")) <> vbBoolean Then SapFail "Execute must be boolean."
    cap = config("maxRows")
    If Not IsNumeric(cap) Then SapFail "Use an integer row cap between 1 and 100."
    cap = CDbl(cap)
    If cap < 1 Or cap > 100 Or Fix(cap) <> cap Then SapFail "Use an integer row cap between 1 and 100."
End Sub

Function SapSmoke(app, config)
    Dim session, transaction, table, maximum, result
    SapValidate config
    Set session = SapSelect(app, config)
    SapWait session
    If session.Info.ScriptingModeReadOnly Then SapFail "Read-only scripting blocks navigation."
    If session.ActiveWindow.Type <> "GuiMainWindow" Then SapFail "Resolve the modal window before navigation."
    transaction = CStr(session.Info.Transaction)
    If transaction <> "SESSION_MANAGER" And transaction <> "SE16" Then SapFail "Start from SAP Easy Access or SE16."
    session.StartTransaction "SE16"
    SapWait session
    SapScreen session
    Set table = session.FindById("wnd[0]/usr/ctxtDATABROWSE-TABLENAME")
    table.Text = config("table")
    If table.Text <> config("table") Then SapFail "Table name was not applied."
    session.FindById("wnd[0]").SendVKey 0
    SapWait session
    SapScreen session
    If session.Info.Transaction <> "SE16" Or session.Info.Program <> "/1BCDWB/DB" & config("table") Or CStr(session.Info.ScreenNumber) <> "1000" Then
        SapFail "Unexpected SE16 selection program/screen; inspect the variant."
    End If
    If config("execute") Then
        Set maximum = session.FindById("wnd[0]/usr/txtMAX_SEL")
        maximum.Text = CStr(CInt(config("maxRows")))
        If CDbl(maximum.Text) <> CDbl(config("maxRows")) Then SapFail "The result limit was not applied; do not execute."
        session.FindById("wnd[0]").SendVKey 8
        SapWait session
        SapScreen session
        If session.Info.Transaction <> "SE16" Or CStr(session.Info.ScreenNumber) = "1000" Then SapFail "Query did not reach a result screen; inspect before retrying."
    End If
    Set result = SapMap()
    result.Add "schema", "sap-gui-windows-se16/v1"
    If config("execute") Then
        result.Add "phase", "query_completed"
        result.Add "maxRows", CInt(config("maxRows"))
    Else
        result.Add "phase", "selection"
        result.Add "maxRows", Null
    End If
    result.Add "table", config("table")
    result.Add "sessionId", CStr(session.Id)
    result.Add "transaction", CStr(session.Info.Transaction)
    result.Add "program", CStr(session.Info.Program)
    result.Add "screenNumber", CStr(session.Info.ScreenNumber)
    result.Add "title", CStr(session.FindById("wnd[0]").Text)
    result.Add "statusText", CStr(session.FindById("wnd[0]/sbar").Text)
    Set SapSmoke = result
End Function

Sub SapReportError(phase, message)
    Dim result
    Set result = SapMap()
    result.Add "schema", "sap-gui-windows-error/v1"
    result.Add "phase", phase
    result.Add "message", message
    WScript.StdErr.WriteLine SapJson(result)
    WScript.Quit 1
End Sub
