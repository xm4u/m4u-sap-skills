# Constants lifecycle, loading, and buffer

## Repository and class

Constants are maintained in `ZSDTCONSTANTE` through maintenance transaction `YBCM006` and must be queried through the static class:

```text
ZBCCL_CONSTANTE_HANDLER
```

The class maintains an **internal read buffer**, which is more efficient than directly querying the constants table at every point in the program.

## Rule: load before querying

Constants must be loaded when initializing the ABAP object. Loading makes the data available in the attribute:

```text
T_CONSTANTE
```

After that, you may:

- read `T_CONSTANTE`;
- use the public methods of `ZBCCL_CONSTANTE_HANDLER`.

## Cumulative loading

Application ID loading is cumulative within the session. Loading an application ID different from those already loaded adds the new set to the buffer's scope.

Do not assume a new load clears the previous buffer.

## Executable program

Preload in `INITIALIZATION`:

```abap
INITIALIZATION.
  CALL METHOD zbccl_constante_handler=>load_constante
    EXPORTING
      i_aplica = 'LMEREPI02'.

  IF sy-subrc <> 0.
    " handle loading errors
  ENDIF.
```

Then, `START-OF-SELECTION` and subsequent routines may query the buffer or class methods.

## Function group

Preload once in the group header/TOP using the `LOAD-OF-PROGRAM` event:

```abap
FUNCTION-POOL zsdgf_test_001.

LOAD-OF-PROGRAM.
  CALL METHOD zbccl_constante_handler=>load_constante
    EXPORTING
      i_aplica = 'LMEREPI02'.

  IF sy-subrc <> 0.
    " handle loading errors
  ENDIF.
```

Do not repeat preloading inside each function module if it can be done once when loading the group.

## Instantiated class

For an instantiated class, load in `CONSTRUCTOR`:

```abap
METHOD constructor.
  CALL METHOD zbccl_constante_handler=>load_constante
    EXPORTING
      i_aplica = 'LMEREPI02'.

  IF sy-subrc <> 0.
    " handle loading errors
  ENDIF.
ENDMETHOD.
```

If the design does not use a suitable instance/constructor, choose a point that guarantees loading happens only once.

## Checklist

- [ ] No repetitive direct `SELECT` against the constants table.
- [ ] `ZBCCL_CONSTANTE_HANDLER` is used.
- [ ] Loading occurs before the first use.
- [ ] Loading occurs once per appropriate lifecycle.
- [ ] `SY-SUBRC` is checked after `LOAD_CONSTANTE`.
- [ ] The code uses the buffer and does not unnecessarily reload the same ID.
