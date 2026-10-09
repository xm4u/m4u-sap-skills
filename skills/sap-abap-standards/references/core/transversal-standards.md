# Cross-cutting standards

## 1. ABAP transport request naming

A transport request description must follow this structure:

| Position | Content |
|---|---|
| A | Request type (`WB` Workbench / `CU` Customizing) |
| B | Separator `-` |
| C | SAP module |
| D | One-character space |
| E | Project / REN / Incident / MC |
| F | One-character space |
| G | Short, clear description of the request's contents |
| H | One-character space |
| I | Change version |
| J | One-character space |
| K | Initials of the responsible functional consultant |

Example description: `WB-BC PE-20180988 Comment process X 00 PDG`.

Complete example:

```text
HEDK912381 PCHAUCA 11.03.2019 WB-BC PE-20180988 Comment process X 00 PDG
```

Operational rules:

- a transport request for the same development must accumulate objects from the previous request where applicable, so the latest request contains the objects handled throughout the process;
- when a predecessor request is accumulated, place `*` before the version number;
- if the predecessor request has already reached PRD and adjustments continue for the same requirement, increment the level and reset the version to `00` (`1 00`, `2 00`, etc.).

## 2. Comments

All implemented code must include comments to support understanding and maintenance.

Comments must:

- be clear and concise;
- give an overview of the section's purpose;
- use lowercase according to the comment rule (a sentence may start with an uppercase letter as described in section 2.1.15);
- explain the logic rather than literally repeat each statement.

## 3. Main technical header

Use this header when ABAP code is first implemented in an object. It must be placed in the first editable lines.

Format:

```abap
*&---------------------------------------------------------------------*
*& Development ID: *
*& Module........: *
*& Functional....: *
*& Author........: *
*& Date..........: *
*& Description...: *
*&---------------------------------------------------------------------*
```

Set `Development ID` to the related project, REN, or incident identifier. The `PAT_GEN` pattern includes this preformatted header.

## 4. Change technical header

This header must be added when code is added or changed. Add change markers/IDs in sequence.

Format:

```abap
*&---------------------------------------------------------------------*
*& CHANGES *
*&---------------------------------------------------------------------*
*& Marker....: @001 *
*& Author....: *
*& Functional: *
*& Date......: *
*& Reason....: *
*&---------------------------------------------------------------------*
```

Rules:

- add `CHANGES` only when a change header is first introduced;
- when two developers alternate work on the same object, a new marker may be used to distinguish the code;
- link the change marker to the changed code blocks.

## 5. Change markers

Markers identify and track changes/extensions in code blocks.

### Multi-line blocks

Adding several lines:

```abap
*{ INSERT @001
...
*} INSERT @001
```

Changing several lines:

```abap
*{ REPLACE @001
...
*} REPLACE @001
```

Deleting/commenting out several lines:

```abap
*{ DELETE @001
...
*} DELETE @001
```

### Single-line marker

```abap
DATA: GS_ID TYPE ICON-ID. "INSERT @001
REFRESH GT_LINES.         "REPLACE @001
* CHECK ...               "DELETE @001
```

### Function groups

In function groups, include a reference to the affected function because one group can contain multiple functions.

Example:

```abap
*{ INSERT @001 : YSDRFC_SIFE_LOAD_DATA
...
*} INSERT @001 : YSDRFC_SIFE_LOAD_DATA
```

## 6. Test / temporary objects

- If they are not needed in PRD, they must be created as local objects in `$TMP`.
- Their names must start with `Y`.
- They must be deleted when their temporary use ends.
