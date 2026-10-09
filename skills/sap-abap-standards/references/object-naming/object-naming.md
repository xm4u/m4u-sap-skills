# Customer ABAP object naming

## 3.1 Package

Pattern:

```text
Z[MM][XX..]
```

- `Z`: customer namespace.
- `MM`: SAP module.
- `XX..`: optional description.

Examples: `ZMM`, `ZPPBKO`, `ZSDLOC_PE`, `ZSDVER_CEM`.

Every Y/Z object intended for PRD must belong to a development package.

## 3.2 Transaction

```text
Z[MM][X][NNN]
```

Examples: `ZMMP001`, `ZSDR023`.

- `X`: program/transaction type.
- `NNN`: 3-digit sequence number.

The sequence number must match the program after removing the leading zero from its 4-digit sequence number. Example: program `ZMMR0023` -> transaction `ZMMR023`.

Reuse gaps in the sequence numbers when available.

## 3.3 Program

```text
Z[MM][X][NNNN]
```

Examples: `ZFIR0001`, `ZSDR0023`.

4-digit sequence number.

## 3.4 Include

General reusable include:

```text
ZIN_[X...X]
```

Example: `ZIN_MACRO`.

Structural includes:

```text
[ZMMXNNNN]_[XXX]
```

Examples: `ZSDP0001_TOP`, `ZSDP0001_MAI`.

Interpret suffix `[XXX]` using the include reference table.

## 3.5 Composite Enhancement Implementation

```text
Z[MM]CE_[X...X]
```

Example: `ZMMCE_RESERVATIONS01`.

## 3.6 Enhancement Implementation

```text
Z[MM]EI_TTTT_[X...X]
```

- `TTTT`: enhanced transaction.

Examples: `ZSDEI_VF04_HIDE_BUTTON`, `ZSDEI_VA0X_SAVE_POPUP`.

## 3.7 Table

```text
Z[MM]T_[X...X]
```

Example: `ZCOT_MATERIAL_COST`.

Additional rules:

- define the Enhancement Category before activation;
- choose row/column storage according to the access pattern and aggregate usage;
- enable buffering only for tables with low variability and moderate volume.

### 3.7.1 Table fields

- if the data corresponds to an existing SAP field, keep the standard name, e.g. `BUKRS`;
- for a custom business field, use a suitable name; a length of 5 characters is recommended. Examples: `ALMTS`, `TDATL`.

## 3.8 Table index

```text
Z[NN]
```

Examples: `Z01`, `Z02`.

`NN`: 2-character sequence.

## 3.9 View

```text
Z[MM]V_[X...X]
```

Example: `ZMMV_MATERIAL_PLANT`.

Variants:

- Append view: `ZZ[MM]V_[X...X]`
- Help view: `Z[MM]VH_[X...X]`
- View cluster: `Z[MM]VC_[X...X]`

## 3.10 HANA views

### View DDL

```text
Z[MM]DDL_[X...X]
```

Example: `ZMMDDL_MATERIAL_PLANT`.

Keep a 1:1 relationship between DDL and CDS view, with the same descriptive name for identification.

### CDS view

Use the same naming convention as database views (`Z[MM]V_...`).

## 3.11 Structure

```text
Z[MM]S_[X...X]
```

Example: `ZWMS_MATERIAL_STOCK`.

Define the Enhancement Category before activation.

### Structure append

```text
ZZ[MM]S_[X...X]
```

Fields in the append must start with `ZZ`.

## 3.12 Table type

```text
Z[MM]TT_[X...X]
```

Example: `ZMMTT_RESERVATIONS`.

## 3.13 Data element

```text
ZE_[X...X]
```

Example: `ZE_BANK`.

## 3.14 Domain

```text
ZD_[CCCC][NNN][_D]
```

Examples: `ZD_CHAR255`, `ZD_DEC15_2`.

- `CCCC`: format (see reference table).
- `NNN`: length.
- `_D`: description/literal according to the example.

### Domain with a value range

```text
ZD_AV[XXX]
```

Example: `ZD_AVMONTH`.

Create a custom domain only when no standard domain has the same type and length.

## 3.15 SET/GET parameter ID

SET/GET parameter IDs must **always start with `Z`**. After the prefix, use a mnemonic abbreviation of the parameter; it should be short (for example, 3 characters where feasible). Example: `ZRET`. Do not generate IDs with the `Y` prefix.

## 3.16 Search help

```text
ZH_[X...X]
```

Example: `ZH_USERS`.

## 3.17 Lock object

```text
EZ_[X...X]
```

Example: `EZ_ZSDNUMBER`.

`E` is a mandatory SAP prefix; the description should preferably refer to the locked table.

## 3.18 SAPscript

```text
Z[MM]SS_[X...X]
```

Example: `ZSDSS_CUSTOMS`.

## 3.19 SAPscript style

```text
ZST_[NNN]
```

Example: `ZST_001`.

## 3.20 SmartForm

```text
Z[MM]SF_[X...X]
```

Example: `ZSDSF_CUSTOMS`.

## 3.21 SmartForm style

```text
ZST_[X...X]
```

Example: `ZST_CUSTOMS`.

## 3.22 SmartForm text module

```text
ZMT_[X...X]
```

Example: `ZMT_LETTER_BBVA`.

## 3.23 Standard texts

```text
ZTE_[X...X]
```

Example: `ZTE_C014_C1_PE27`.

## 3.24 Function group

```text
Z[MM]GF_[X...X]
```

Example: `ZHRGF_EMPLOYEES`.

## 3.25 Function module

```text
Z[MM]F_[X...X]
```

Example: `ZFIF_CHECK_PAYMENTS`.

## 3.26 Update function module

```text
Z[MM]UF_[X...X]
```

Example: `ZFIUF_REFERENCE`.

## 3.27 RFC function module

```text
Z[MM]RFC_[X...X]
```

Examples: `ZSDRFC_DOC_TYPE`, `ZSDRFC_CLWB_DOC_TYPE`, `ZMMRFC_ACOP_DATA`.

## 3.28 BTE function module

```text
Z[MM]F_BTE_[X...X]_Y_NN
```

- `[X...X]`: standard BTE to copy;
- `Y`: `P` process or `E` event;
- `NN`: optional 2-digit sequence number.

Examples: `ZFIF_BTE_00001020_E_00`, `ZFIF_BTE_00001020_P_03`.

## 3.29 BSP application

```text
Z[MM]BSP_[X...X]
```

Example: `ZMMBSP_RELEASE_PO`.

## 3.30 BAdI implementation

```text
Z[X...X][N]
```

`N`: optional 1-digit sequence number.

Example for `ME_PROCESS_PO_CUST`: `ZME_PROCESS_PO_CUST`.

## 3.31 Class and interface

```text
Z[MM]CL_[X...X]
Z[MM]IF_[X...X]
```

Examples: `ZSDCL_BUILD_REPORT`, `ZSDIF_REPORTS`.

Alphanumeric characters, `_`, and `/` are permitted in general class/interface names; names must not start with a digit.

## 3.32 Business Object

```text
ZBO_[X...X]
```

Example: `ZBO_CRM`.

## 3.33 Enterprise Service

```text
Z[MM][AA]_[X...X]
```

- `DS`: SAP service definition;
- `CO`: external service consumer.

Specific rules:

- for consumers, use prefix `Z` + module (`ZMM`, `ZSD`, `ZCO`);
- for projects, include four characters identifying the project, separated by `_`.

Examples:

- `ZSDDS_CREATE_ORDER`
- `ZSDDS_CRVJ_DELETE_ORDER`
- `ZSDCO_QUERY_CPB_STATUS`

## 3.34 OData SAP Gateway Service

```text
Z[MM]GS_[ZZZZZ]_[X...X]
```

Example: `ZMMGS_CRVJL_PO`.

### Data modeling components

Rules:

- CamelCase;
- no underscores;
- English names;
- do not use technical SAP names.

Entities:

- nouns only;
- singular;
- do not include operations.

Examples: `SalesOrderHeader`, `SalesOrderItem`, `Address`, `CostCenter`.

Complex types: use them to group fields when an entity has too many.

Entity Sets:

- plural, or a `Set` suffix.

Examples: `SalesOrderHeaders`, `Addresses`, `CurrencySet`.

Navigations:

- target cardinality 1: same as the entity name;
- target cardinality M: same as the entity set.

Function Imports: the name must clearly indicate the operation, e.g. `ReleasePO`, `ApproveLeave`, `BlockSalesOrder`, `GetReleaseStatus`.

Service Implementations: apply class method and ABAP performance rules.

Runtime Artifacts:

```text
Z[MM]CL_[YYYYY_Y...Y]_[KKK]
```

Suffixes:

- `_DPC`
- `_DPC_EXT`

Example for `ZMMGS_CRVJL_PO`:

- `ZMMCL_CRVJL_PO_DPC`
- `ZMMCL_CRVJL_PO_DPC_EXT`

## 3.35 CMOD enhancement object

```text
Z[MM][NNN]
```

Example: `ZSD001`.

3-digit sequence number.

## 3.36 Query user group

```text
Z[MM]GU_[X...X]
```

Example: `ZSDGU_SALES`.

## 3.37 Query InfoSet

```text
Z[MM]IS_[X...X]
```

Example: `ZSDIS_SALES_DOC`.

## 3.38 Query

```text
Z[MM]Q_[X...X]
```

Example: `ZSDQ_DELIVERIES`.

## 3.39 LSMW project

```text
ZP_[X...X]
```

Example: `ZP_LEANSA`.

## 3.40 LSMW subproject

```text
Z[MM]SP_[X...X]
```

Example: `ZMMSP_ORDERS`.

## 3.41 LSMW object

```text
Z[MM]O_[X...X]
```

Example: `ZMMO_ME21N_01`.

## 3.42 Authorization object

```text
Z[MM]_[X...X]
```

Example: `ZMM_WERKS`.

Notes:

- consider `ACTVT` for finer restrictions;
- the data being validated must refer to a standard element.

## 3.43 Message class

```text
Z[MM][NN]
```

Example: `ZPP01`.

Prefer one class per module.

Message numbers: `001` to `999`.

## 3.44 Variant

Free text.

## 3.45 Type group

```text
Z[MM][NN]
```

Example: `ZWM01`.

## 3.46 Standard texts

```text
ZTE_[X...X]
```

Example: `ZTE_C014_C1_PE27`.

## 3.47 Graphics

```text
ZGH_AAAA_[X...X]
```

- `AAAA`: graphic type (`Logo`, `Sign` for signature, or empty for a generic graphic).

Examples: `ZGH_IMAGE001`, `ZGH_LOGOS_PE27`, `ZGH_SIGN_USER01`.

## 3.48 Area menu

```text
ZMM_MENU_[XXXXX]
```

Example: `ZMM_MENU_INTERCOMPANY_SALES`.
