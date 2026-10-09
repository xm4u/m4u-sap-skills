# Include `_MAI` - Validations and events

## 4.4.1 Initialization and screen validation

`_MAI` contains validation and initialization events.

Template:

```abap
INITIALIZATION.
  PERFORM INITIALIZE.

AT SELECTION-SCREEN OUTPUT.

AT SELECTION-SCREEN ON VALUE-REQUEST FOR P_WAERS.
  PERFORM HELP_WAERS USING P_WAERS.

AT SELECTION-SCREEN ON BLOCK B_01.

AT SELECTION-SCREEN ON P_BUKRS.

AT SELECTION-SCREEN.
```

Rules:

- all input parameter validation must run in these events to return errors/information on the selection screen;
- FORMs may be created to group validations by event;
- `INITIALIZATION` loads values/variables before use;
- load the program's constants globally here, following the constants procedure.

## 4.4.2 Main routine

It must begin with:

```abap
START-OF-SELECTION.
```

The main block handles data extraction or the core development logic.

Rules:

- comment the main block;
- if it uses a logical database (BDL), document the logical database and screen;
- store retrieved data in an internal table;
- modularize through methods or PERFORMs;
- after selection, check success before further processing.

## 4.4.3 Data processing

Located in:

```abap
END-OF-SELECTION.
```

Rules:

- check that data exists;
- if it does not, stop with an appropriate message;
- enrich, sort, and process data in subroutines;
- separate output/report generation into an additional subroutine.

## 4.4.4 Control events

Possible events after output:

```abap
TOP-OF-PAGE.
END-OF-PAGE.
TOP-OF-PAGE DURING LINE-SELECTION.
AT LINE-SELECTION.
AT PFNN.
AT USER-COMMAND.
```

Implement only the required events, not all of them. These events have no mandatory ordering.
