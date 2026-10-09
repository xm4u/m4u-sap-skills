# ABAP4/SAP internal naming convention

Where a related SAP field exists, its name should be reused in the free part of the name. Example: `GS_BUKRS`.

## Internal tables

| Scope | Type | Prefix |
|---|---|---|
| global | unspecified type | `gt_` |
| global | standard | `gdt_` |
| global | sorted | `gst_` |
| global | hashed | `ght_` |
| local | unspecified type | `lt_` |
| local | standard | `ldt_` |
| local | sorted | `lst_` |
| local | hashed | `lht_` |
| static | unspecified type | `st_` |
| static | standard | `sdt_` |
| static | sorted | `sst_` |
| static | hashed | `sht_` |

## Structures

- global: `gwa_<name>`
- local: `lwa_<name>`
- static: `swa_<name>`

## Scalar variables

### Global

- character `C`: `gs_`
- numeric text `N`: `gn_`
- date `D`: `gd_`
- time `T`: `gh_`
- hexadecimal `X`: `gx_`
- integer `I`: `gi_`
- packed number `P`: `gp_`
- floating point `F`: `gf_`
- other: `g_`

### Local

- `C`: `ls_`
- `N`: `ln_`
- `D`: `ld_`
- `T`: `lh_`
- `X`: `lx_`
- `I`: `li_`
- `P`: `lp_`
- `F`: `lf_`
- other: `l_`

### Static

- `C`: `ss_`
- `N`: `sn_`
- `D`: `sd_`
- `T`: `sh_`
- `X`: `sx_`
- `I`: `si_`
- `P`: `sp_`
- `F`: `sf_`
- other: `s_`

## FORM parameters

- `USING`: `pi_<name>`
- `CHANGING`: `po_<name>`

`TABLES` is prohibited. Do not define FORM parameters with `TABLES`; when passing an internal table, use a typed parameter through `USING` or `CHANGING` according to its direction of use.

## Selection screen and ranges

- `PARAMETERS`: `p_<name>`
- `SELECT-OPTIONS`: `s_<name>`
- selection screen block: `b_<name>`
- global range: `gr_<name>`
- local range: `lr_<name>`
- static range: `sr_<name>`

## Constants

- global: `gc_<name>`
- local: `lc_<name>`

## Field symbols

- global: `<g_<object>>`
- local: `<l_<object>>`

Example: `<g_matnr>`.

## Subroutines, macros, and types

- subroutine: descriptive name; other sections require an infinitive verb + object;
- macro: `M_<name>`;
- global type: `gty_<name>`;
- local type: `lty_<name>`.

## Table types

### Global

- unspecified type: `gtyt_`
- standard: `gtyd_`
- sorted: `gtys_`
- hashed: `gtyh_`

### Local

- unspecified type: `ltyt_`
- standard: `ltyd_`
- sorted: `ltys_`
- hashed: `ltyh_`

## Classes and objects

- global class: `gcl_`
- local class: `lcl_`
- global object: `go_`
- local object: `lo_`
- static object: `so_`

## Function module parameters

Importing:

- parameter: `IP_`
- structure: `IW_`
- table: `IT_`

Exporting:

- parameter: `EP_`
- structure: `EW_`
- table: `ET_`

Modify:

- parameter: `MP_`
- structure: `MW_`
- table: `MT_`

Do not use the `TABLES` interface section in function modules. For tables, define typed parameters in `IMPORTING`, `EXPORTING`, or `CHANGING`, as appropriate.

## Class method parameters

Importing:

- parameter: `IP_`
- structure: `IW_`
- table: `IT_`
- class: `IC_`

Exporting:

- parameter: `EP_`
- structure: `EW_`
- table: `ET_`
- class: `EC_`

Changing:

- parameter: `CP_`
- structure: `CW_`
- table: `CT_`
- class: `CC_`

Returning:

- parameter: `RP_`
- structure: `RW_`
- table: `RT_`
- class: `RC_`
