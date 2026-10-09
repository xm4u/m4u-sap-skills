# Naming reference tables

## Table 1 - Modules

| Code | Description |
|---|---|
| `BC` | General use |
| `BW` | Business Warehouse |
| `CO` | Controlling |
| `CS` | Customer Service |
| `FI` | Finance |
| `HR` | Human Resources |
| `MM` | Materials |
| `PM` | Maintenance |
| `PP` | Production |
| `PS` | Project Management |
| `QM` | Quality |
| `SD` | Sales and Distribution |
| `WM` | Warehouse Management |

## Table 2 - Program / transaction type

Valid for programs or transactions:

| Code | Name | Use |
|---|---|---|
| `B` | Batch | Batch Input, Call Transaction, etc. |
| `P` | Processes and other developments | various specific processes/activities |
| `F` | Form | generates SmartForms or SAPscript |
| `R` | Report | data selection and listing |
| `M` | Table maintenance | table maintenance/initial load |
| `S` | Subroutine pool | contains subroutines called by other applications |

Valid for BW programs:

- `DR`: Actual Data
- `DM`: Master Data

Transactions only:

- `A`: Table update
- `Q`: Query

## Table 3 - Format type

| Code | Description | Specified ID |
|---|---|---|
| `CHAR` | string | `C` |
| `CURR` | currency, stored as DEC | - |
| `DATS` | date YYYYMMDD as CHAR(8) | `D` |
| `DEC` | signed calculation/amount | `P` |
| `FLTP` | 8-byte floating point | `F` |
| `INT` | integer | `I` |
| `NUMC` | digit-only string | `N` |
| `QUAN` | quantity with unit | - |
| `TIMS` | time HHMMSS as CHAR(6) | `T` |
| `UNIT` | unit for QUAN | `U` |

## Table 4 - Valid customer packages

`ZBC`, `ZBW`, `ZCO`, `ZCS`, `ZFI`, `ZHR`, `ZIM`, `ZLE`, `ZMM`, `ZPM`, `ZPP`, `ZPS`, `ZQM`, `ZSD`, `ZTR`, `ZWM`.

## Table 5 - Includes and contents

| Suffix | Contents |
|---|---|
| `_TOP` | initial declarations |
| `_SEL` | selection parameters |
| `_MAI` | main process and events |
| `_F01` | subroutines |
| `_O01` | Process Before Output |
| `_I01` | Process After Input |
| `_CLA` | method/class implementation |
