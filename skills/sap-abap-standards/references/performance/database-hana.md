# Database and SAP HANA performance

## Keep result sets small

- do not retrieve full rows only to discard them on the application server;
- make the `WHERE` clause as specific as possible.

## Minimize transferred data

- select only the required columns; avoid `SELECT *`;
- use database aggregate functions (`COUNT`, `MIN`, `MAX`, `SUM`, `AVG`) where appropriate instead of transferring rows for calculations in ABAP.

## Minimize access count

Each database access has overhead. Rules:

- prefer `JOIN` and/or subqueries over nested `SELECT` statements;
- avoid repeated access to the same data;
- consider ABAP table buffering where applicable;
- use `FOR ALL ENTRIES` instead of many `SELECT` / `SELECT SINGLE` calls where appropriate;
- replace nested `SELECT SINGLE` calls with a suitable SQL construct;
- use array operations for `INSERT`, `UPDATE`, `MODIFY`, and `DELETE`.

## Indexes

As a design guideline, HANA normally does not require many secondary indexes. They may be beneficial for highly selective queries on non-key fields.

When designing Y/Z tables:

- avoid excessive indexes;
- for row storage, aim for key-based access; otherwise, review an appropriate index for the access pattern;
- if a `JOIN` is required, check whether a Dictionary view already covers the tables.

## SELECT and WHERE

- use an explicit field list;
- `SELECT SINGLE` is recommended when only one row is needed, but selection fields must still be specified;
- put conditions in `WHERE` instead of retrieving data and filtering with `CHECK`;
- use SQL calculation functions where appropriate;
- avoid repeatedly accessing the same record, even with `SELECT SINGLE`.

## Keys and indexes

- use the first `n` fields of an index/key in `WHERE` where possible;
- follow the field order defined for the key or index;
- try the complete primary key or index first, then partial access in the defined order;
- the field order in `SELECT` must also match the table's physical order and the target internal table.

## `INTO CORRESPONDING FIELDS`

Normal use of `INTO CORRESPONDING FIELDS` is permitted when it simplifies mapping a `SELECT` result into a compatible structure or internal table. It must not be reported as a performance issue on its own. Still use an explicit field list in `SELECT` and select only the required data.

## `FOR ALL ENTRIES`

`FOR ALL ENTRIES` is permitted as a normal alternative for preloading data and avoiding repeated access. Its mandatory precondition is to check that the driver table contains entries.

- always check that the driver table is not empty;
- remove duplicates before FAE to limit access;
- remember that FAE performs an implicit `DISTINCT`, so take care when selecting key fields;
- explicitly specify `SELECT DISTINCT` when intended.

## Reduce database load / HANA balance

- avoid redundant reads;
- use table buffering where appropriate and do not bypass it without a reason;
- sort data in ABAP when that is more efficient;
- in HANA, move data-intensive calculations to the database, but avoid repeating the same operation in redundant contexts;
- perform sorting in HANA when it determines the result (for example, top N) or is part of a larger calculation.

## Code-to-Data

Selection priority:

1. Open SQL.
2. CDS / AMDP only when they provide concrete value.

CDS/AMDP are justified when they:

- provide database-specific functions unavailable in Open SQL;
- replace intensive processes involving repeated transfers of large volumes;
- are reusable.
