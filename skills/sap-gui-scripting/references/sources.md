# Sources and compatibility

## Official SAP references

- [SAP GUI for Java: introduction](https://help.sap.com/docs/sap_gui_for_java/e665f2b67dbd4328ab6bd9e029b84581/25f72ad2ab594579b96f7da4c71afa59.html): Java client platforms and runtime.
- [Java scripting](https://help.sap.com/docs/sap_gui_for_java/e665f2b67dbd4328ab6bd9e029b84581/93d76aa9e297464f8968a6c11a607c3e.html): built-in engine and opening, recording, editing, replaying scripts.
- [Web AS ABAP preferences](https://help.sap.com/docs/sap_gui_for_java/e665f2b67dbd4328ab6bd9e029b84581/fc47e854e41a41eda017c7c112bdbeaf.html): scripting setting, notifications, recording ID formats and directories.
- [SAP GUI Scripting API](https://help.sap.com/docs/sap_gui_for_windows/b47d018c3b9b45e897faf66a6c0885a8?locale=en-US): object model and Java/Windows support differences. Much of this documentation uses Windows declarations; check the Java implementation before relying on a signature.
- [SapGuiAuto object](https://help.sap.com/docs/sap_gui_for_windows/b47d018c3b9b45e897faf66a6c0885a8/cc21a893b44f435e85daceb2305f1026.html): Windows Running Object Table attachment and `GetScriptingEngine`.
- [GuiSession object](https://help.sap.com/docs/sap_gui_for_windows/b47d018c3b9b45e897faf66a6c0885a8/a4e022f6c155414d9c8ae8eba422cac5.html): Windows session metadata, `Busy`, `FindById`, and transaction navigation.
- [Requirements and remarks](https://help.sap.com/docs/sap_gui_for_windows/b47d018c3b9b45e897faf66a6c0885a8/45a62269a13d4522997bedf3e6ff56f8.html?locale=en-US&state=PRODUCTION&version=800.05): server restrictions and relevant SAP notes.
- [Server protection mode combinations](https://help.sap.com/docs/sap_gui_for_windows/1f190e2f59db43e192cba638ea29870b/76d8d2b932ce4e71b91c313d818a51f2.html): per-user/read-only behavior. Its Windows-specific registry instructions are not macOS setup steps.

Use documentation belonging to the target release and inspect the target client's recording/API when a method is uncertain. Do not treat Personas scripting APIs or Windows COM declarations as an interchangeable Java API.

The installed Java 8.10 rev13 native launcher's `--help` lists `-f`/`-F` and `-s`/`-S`. A live shell launch confirmed a new process with zero connections rather than access to the existing authenticated client. The [Java file bridge](java-shell-runtime.md) is this repository's adapter using the verified built-in engine plus standard Java interop; it is not an official SAP external API. [Nashorn Java interop](https://docs.oracle.com/javase/8/docs/technotes/guides/scripting/nashorn/api.html) documents `Java.type`, `Java.to`, and `Java.extend`; availability was checked in the installed client.

## Upstream inspiration

The user supplied [efeumutaslan/SAP-SKILLS: sap-gui-scripting](https://github.com/efeumutaslan/SAP-SKILLS/blob/main/skills/sap-gui-scripting/SKILL.md) as an initial reference. Its Windows COM/VBScript/Python examples provide conceptual context. This skill has separate Java and Windows adapters. The upstream instruction to disable notifications and its hardcoded first-session selection are not prerequisites here.

## Validation baseline

On 2026-10-09, SAP GUI for Java **8.10 rev13 on macOS** was inspected locally. The installed Java scripting wrappers were checked read-only to confirm lower-camel-case properties, `children.length`/`elementAt`, session metadata, `startTransaction`, `findById`, and window `sendVKey` availability. Live session inspection returned a reachable authenticated session and effective scripting flags.

This is a compatibility baseline, not a promise that every SAP GUI for Java revision, system, screen variant, language, ALV control, or operating system behaves identically. Java on Windows/Linux still requires separate validation.

Also on 2026-10-09, the local Java file bridge passed shell status and session inspection in the authenticated macOS client. Python returned one session and no inventory errors without per-script editor interaction. The transport baseline does not prove SE38 editing, activation or business changes; see [shell execution](java-shell-runtime.md#validation).

On the same date, native SAP GUI for Windows **8.10 64-bit** passed COM attachment, session inspection, and SE16/VBAK display of ten rows using WSH VBScript. See the [SE16 example](se16-example.md) for both live outcomes and binary versions, and [Windows execution](windows-runtime.md) for the observed PowerShell COM binding limitation. WSH availability, other hosts, versions, and screen variants need separate validation.
