# Constants access patterns

These patterns illustrate preloading constants and querying the buffer for each ABAP object type.

## 1. Program: preload + buffer read

```abap
REPORT zpch0001.

PARAMETERS:
  p_hkont TYPE hkont.

INITIALIZATION.
  CALL METHOD zbccl_constante_handler=>load_constante
    EXPORTING
      i_aplica = 'LMEREPI02'.

  IF sy-subrc <> 0.
    " handle loading errors
  ENDIF.

START-OF-SELECTION.
  READ TABLE zbccl_constante_handler=>t_constante
    TRANSPORTING NO FIELDS
    WITH KEY aplica  = 'LMEREPI02'
             cgroup  = 'HKONT'
             zvalor  = p_hkont.

  IF sy-subrc = 0.
    " execute the process
  ENDIF.
```

## 2. Function group: single load

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

Subsequent function modules may query `T_CONSTANTE` without reloading the same scope.

## 3. Class: constructor + subsequent use

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

Then, in another method:

```abap
METHOD get_data.
  READ TABLE zbccl_constante_handler=>t_constante
    TRANSPORTING NO FIELDS
    WITH KEY aplica = 'LMEREPI02'
             cgroup = 'HKONT'
             zvalor = i_hkont.

  IF sy-subrc = 0.
    " execute the process
  ENDIF.
ENDMETHOD.
```

## 4. Review rules

- Preloading must be separate from repetitive business logic.
- Do not reload constants in every iteration or call if they can already reside in the buffer.
- Using `T_CONSTANTE` is valid under this procedure.
- Public methods are a valid alternative to reading `T_CONSTANTE` manually.
- Parameter names may vary between methods; use the actual signature of the installed class.
