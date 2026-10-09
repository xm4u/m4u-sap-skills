# ZBCCL_CONSTANTE_HANDLER methods

## API used by this procedure

The public static methods used are:

- `CHECK_VALUE`
- `GET_VALUE_ZVALOR`
- `GET_VALUE_YVALOR`
- `GET_VALUE_SINGLE`
- `GET_RANGE_REF`
- `LOAD_CONSTANTE`

You may also access `T_CONSTANTE` directly after preloading.

> Before generating a new call, validate the actual signature of the class available in SAP. Do not invent parameter names when repository code shows a different signature.

## LOAD_CONSTANTE

Loads active constants for an application/group into the class buffer.

Example pattern:

```abap
CALL METHOD zbccl_constante_handler=>load_constante
  EXPORTING
    i_aplica = 'LMEREPI02'.

IF sy-subrc <> 0.
  " handle errors
ENDIF.
```

## CHECK_VALUE

Checks whether an active value exists within a constants group.

A return value of `0` indicates that the value exists:

```abap
IF zbccl_constante_handler=>check_value(
     i_zaplica = 'LMEREPI02'
     i_cgroup  = 'TCODE'
     i_zvalor  = '25' ) = 0.
  " constant exists
ENDIF.
```

`I_ZVALOR` and `I_YVALOR` may be evaluated independently.

## GET_VALUE_ZVALOR

Returns `ZVALOR` from the first active record matching the specified group/filter.

The example filters by `YVALOR`:

```abap
ls_vkbur_alt = zbccl_constante_handler=>get_value_zvalor(
  i_zaplicacion = 'ZSD_SALES'
  i_zcgrupo     = 'VKBURX'
  i_yvalor      = '06' ).
```

The example's expected result is `25`.

## GET_VALUE_YVALOR

Returns `YVALOR` from the first active record matching the specified group/filter.

The example filters by `ZVALOR`:

```abap
ls_vkbur_alt = zbccl_constante_handler=>get_value_yvalor(
  i_zaplicacion = 'ZSD_SALES'
  i_zcgrupo     = 'VKBURX'
  i_zvalor      = '25' ).
```

The example's expected result is `06`.

## GET_VALUE_SINGLE

Returns the complete record queried by sequence number.

If no sequence number is supplied, it returns the first active record in the queried group.

```abap
lwa_es_data = zbccl_constante_handler=>get_value_single(
  i_zaplicacion   = 'ZSD_SALES'
  i_zcgrupo       = 'VKBURX'
  i_zcorrelativo  = '001' ).
```

## GET_RANGE_REF

Returns records as a reference object pointing to a range. `I_REF_RSTRUC` defines the range structure.

Parameters used:

- `I_ZAPLICACION`
- `I_ZCGRUPO`
- `I_REF_RSTRUC`
- `E_REF_DATA` as the reference result

`I_SIGN` and `I_OPTION` may also be used to define how range values are evaluated.

Example pattern:

```abap
DATA:
  ldt_r_bsart TYPE STANDARD TABLE OF edm_bsart_range,
  lo_r_data   TYPE REF TO data.

FIELD-SYMBOLS:
  <fs_r_data> TYPE ANY TABLE.

zbccl_constante_handler=>get_range_ref(
  EXPORTING
    i_zaplicacion = 'MGCPUR005'
    i_zcgrupo     = 'BSARTP'
    i_ref_rstruc  = 'EDM_BSART_RANGE'
  RECEIVING
    e_ref_data    = lo_r_data ).

ASSIGN lo_r_data->* TO <fs_r_data>.
IF <fs_r_data> IS ASSIGNED.
  ldt_r_bsart[] = <fs_r_data>[].
ENDIF.
```

## Choosing a method

| Need | Method |
|---|---|
| Preload constants/buffer | `LOAD_CONSTANTE` |
| Check whether an active value exists | `CHECK_VALUE` |
| Get `ZVALOR` | `GET_VALUE_ZVALOR` |
| Get `YVALOR` | `GET_VALUE_YVALOR` |
| Get a complete record | `GET_VALUE_SINGLE` |
| Build a dynamic range | `GET_RANGE_REF` |
| Apply specific logic to several records already loaded | read `T_CONSTANTE` |
