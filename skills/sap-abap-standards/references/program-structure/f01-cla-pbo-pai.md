# F0n, CLA, O01, and I01 includes

## 4.5 `_F0n` - Subroutines

Contains all internal subroutines called by the program.

Each FORM must have a header documenting:

- main functionality;
- input parameters;
- output parameters.

Template:

```abap
*----------------------------------------------------------------------*
* Form SUBROUTINE
*----------------------------------------------------------------------*
* document the subroutine functionality here
*----------------------------------------------------------------------*
* --> p1 document input parameters
* <-- p2 document output parameters
*----------------------------------------------------------------------*
FORM SUBROUTINE USING PI_PAR1 PI_PAR2.
  DATA LD_FIELD1 TYPE D. " comment
  ...
ENDFORM. " SUBROUTINE
```

## 4.6 `_CLA` - Class implementation

Contains implementations of program classes previously defined in `_TOP`.

Conceptual template:

```abap
CLASS LCL_CX IMPLEMENTATION.
  METHOD CONSTRUCTOR.
    ...
  ENDMETHOD.
ENDCLASS.
```

## 4.7 `_O01` - Process Before Output

Contains PBO modules.

Example:

```abap
MODULE STATUS_1004 OUTPUT.
  SET TITLEBAR 'TIT1004'.
  SET PF-STATUS 'GUI1004'.
ENDMODULE.
```

## 4.8 `_I01` - Process After Input

Contains PAI modules.

Example:

```abap
MODULE USER_COMMAND_1004 INPUT.
  CASE OK_CODE.
    WHEN 'BACK'.
      LEAVE TO SCREEN 0.
    WHEN 'EXIT'.
      LEAVE PROGRAM.
    WHEN 'CANC'.
      LEAVE TO SCREEN 0.
  ENDCASE.
ENDMODULE.
```

## Reference suffixes

- `_TOP`: initial declarations.
- `_SEL`: selection parameters.
- `_MAI`: main process and events.
- `_F01`: subroutines.
- `_O01`: PBO.
- `_I01`: PAI.
- `_CLA`: class/method implementation.
