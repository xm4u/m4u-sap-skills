# Main program, TOP, and SEL

## 4.1 Main program

The main program is called by the transaction. It contains:

- technical header;
- modularization includes.

Template:

```abap
REPORT ZMMZNNNN MESSAGE-ID ZMM
  LINE-SIZE 132 LINE-COUNT 65
  NO STANDARD PAGE HEADING.

"INCLUDE <icon>.          " global libraries
"INCLUDE ZMMZNNNN_TOP.    " global data
"INCLUDE ZMMZNNNN_SEL.    " selection screen
"INCLUDE ZMMZNNNN_MAI.    " main program
"INCLUDE ZMMZNNNN_CLA.    " class implementation
"INCLUDE ZMMZNNNN_F01.    " subroutines
"INCLUDE ZMMZNNNN_O01.    " PBO
"INCLUDE ZMMZNNNN_I01.    " PAI
```

## 4.2 Include `_TOP`

Contains global constants and variables.

Organization:

1. tables / data structures used by the program;
2. constants;
3. global variables;
4. types;
5. table types;
6. internal tables;
7. structures/work areas;
8. ranges;
9. field symbols;
10. field groups, if applicable.

Rules:

- every declared table has a brief descriptive comment on the right;
- every added object must be commented;
- where possible, define variables with references to DDIC fields through `TYPE`;
- `OCCURS` is completely prohibited; use modern internal table definitions without header lines;
- do not declare `TABLES:` in `_TOP`; `TABLES` is prohibited and must be replaced with explicitly typed work areas/structures;
- field symbols are recommended for modifying internal tables where possible, for performance.

Abbreviated example:

```abap
CONSTANTS:
  GC_SOBKZ TYPE QBEW-SOBKZ VALUE 'Q'.

DATA:
  GS_BUKRS TYPE T001-BUKRS. " comment

TYPES:
  BEGIN OF GTY_MAKT,
    MATNR TYPE MAKT-MATNR,
    MAKTX TYPE MAKT-MAKTX,
  END OF GTY_MAKT.

DATA:
  GDT_MARC TYPE STANDARD TABLE OF GTY_MARC,
  GHT_MARC TYPE HASHED TABLE OF GTY_MARC WITH UNIQUE KEY MATNR WERKS,
  GST_MARC TYPE SORTED TABLE OF GTY_MARC WITH NON-UNIQUE KEY MATNR.
```

## 4.3 Include `_SEL`

Contains all initial screen fields:

- `PARAMETERS`;
- `SELECT-OPTIONS`;
- selection screen blocks;
- radio buttons / checkboxes where applicable.

Rules:

- do not create a program without at least one selection parameter, to prevent accidental execution and display a screen with a title/fields first;
- order `PARAMETERS` and `SELECT-OPTIONS` by their visual position;
- comment each parameter;
- use parameters as an alternative to hardcoded values;
- `DEFAULT` is permitted when useful for initializing a parameter or selection control.

Block template:

```abap
SELECTION-SCREEN BEGIN OF BLOCK B_01 WITH FRAME TITLE TEXT-001.
PARAMETERS: P_BUKRS TYPE T001-BUKRS OBLIGATORY DEFAULT '10',
            P_WERKS TYPE T001W-WERKS MEMORY ID WRK OBLIGATORY.
SELECT-OPTIONS: S_BKLAS FOR MBEW-BKLAS NO INTERVALS NO-EXTENSION,
                S_MATNR FOR MSEG-MATNR.
SELECTION-SCREEN END OF BLOCK B_01.
```
