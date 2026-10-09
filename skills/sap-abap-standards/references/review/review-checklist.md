# Comprehensive review checklist

This checklist is an operational index. Detailed rules are in the topic-specific guides.

## A. Traceability and changes

- [ ] Main technical header present where applicable.
- [ ] `Development ID`, module, functional consultant, author, date, and description provided.
- [ ] `CHANGES` header for subsequent changes.
- [ ] Sequential `INSERT` / `REPLACE` / `DELETE` markers.
- [ ] Function group markers reference the affected function.
- [ ] Clear and consistent comments.

## B. Internal naming

- [ ] Correct global/local/static prefixes.
- [ ] Internal tables distinguish standard/sorted/hashed where applicable.
- [ ] Structures/work areas, types, classes, and objects follow prefixes.
- [ ] Method/function parameters follow IP/IW/IT, EP/EW/ET, CP/CW/CT, RP/RW/RT, etc.

## C. Quality

- [ ] `TYPE` instead of `LIKE` where required by the standard.
- [ ] No `RANGES`; use `TYPE RANGE OF`.
- [ ] No `OCCURS` in any form and no legacy header lines.
- [ ] No `TABLES` declarations or parameters; use work areas and typed parameters.
- [ ] Typed field symbols.
- [ ] Internal tables without header lines and with explicit type/key.
- [ ] Hardcoded values avoided or converted into constants/parameters.
- [ ] `DEFAULT` on selection screens is valid when it provides a useful initial value.
- [ ] `MOVE-CORRESPONDING` avoided unless field-by-field assignment makes the transfer excessively complex.
- [ ] One main process per FORM.
- [ ] Reasonable nesting.
- [ ] One statement per line and consistent indentation.
- [ ] Messages through message classes/message IDs.
- [ ] UI literals through text elements.
- [ ] Justified dead code.
- [ ] Variables/declarations commented according to the standard.

## D. Critical statements

- [ ] `FOR ALL ENTRIES` may be used normally and is protected against an empty driver table.
- [ ] Duplicates removed before FAE where applicable.
- [ ] Empty range checked before `IN` when it could cause a full scan.
- [ ] Division by zero / overflow handled.

## E. Performance

- [ ] `SELECT` with a field list, not `*`, unless an exception is justified under this repository's criteria.
- [ ] Specific `WHERE` clause.
- [ ] `INTO CORRESPONDING FIELDS` accepted when it simplifies mapping; not penalized on its own.
- [ ] No `SELECT` inside loops when data can be preloaded.
- [ ] JOIN/subquery/FAE considered as appropriate.
- [ ] Database array operations where applicable.
- [ ] Index/key fields used in the appropriate order according to the standard.
- [ ] Sorted STANDARD TABLE + BINARY SEARCH for relevant searches.
- [ ] SORT specifies `BY` and direction where applicable.
- [ ] `LOOP ... WHERE` preferred over `LOOP` + `CHECK`.
- [ ] Efficient table copies and partial modifications.

## F. Configuration constants

If the code uses configuration constants:

- [ ] `ZBCCL_CONSTANTE_HANDLER` used instead of repetitive direct queries against the constants table.
- [ ] Preloading occurs before the first use.
- [ ] Program: load in `INITIALIZATION`.
- [ ] Function group: load once in `LOAD-OF-PROGRAM`.
- [ ] Instantiated class: load in `CONSTRUCTOR` or an equivalent single-load point.
- [ ] Loading call is `LOAD_CONSTANTE`; no nonexistent `LOAD_OF_PROGRAM` method is generated.
- [ ] `SY-SUBRC` checked after loading.
- [ ] Same ID not unnecessarily reloaded in loops/repeated routines.
- [ ] Appropriate method or preloaded `T_CONSTANTE` used for existence/values/records/ranges.
- [ ] Method signatures not invented when they require SAP system validation.

## G. Security and authorizations

For Z programs/transactions:

- [ ] One or more `AUTHORITY-CHECK` statements according to the protected information/action.
- [ ] Authorization object matches the module/scope.
- [ ] `ACTVT` represents the executed action.
- [ ] Each sensitive action has its specific check when multiple activities exist.
- [ ] `SY-SUBRC` evaluated immediately after `AUTHORITY-CHECK`.
- [ ] Authorization failure prevents the operation from continuing.
- [ ] Transaction/object/values/activities must be registered in `SU24` (SAP verification).

For maintenance views:

- [ ] SU24 includes `S_TABU_NAM`.
- [ ] `TABLE` references the table actually maintained.
- [ ] Only necessary activities (`01` create, `02` change, `03` display, where applicable).

## H. Modularization

- [ ] Main program composed of processes at the same abstraction level.
- [ ] Each module has one main responsibility.
- [ ] Global variables used only when justified.
- [ ] Parameter passing makes reads/changes explicit.
- [ ] Reusable components are parameterized and free of hardcoded values.

## I. Object naming

- [ ] Correct package/module.
- [ ] Program/transaction sequence numbers match.
- [ ] Include uses the main program name + correct suffix.
- [ ] DDIC/class/function/RFC/BAdI/OData/etc. follow their specific patterns.
- [ ] Customer authorization objects follow `Z[MM]_[X...X]`.
- [ ] SET/GET parameter IDs always start with `Z`.
- [ ] Sequence numbers not invented without checking availability.

## J. Program structure

If the program is new and has events or >500 lines:

- [ ] main program with header and includes;
- [ ] `_TOP` contains only global declarations;
- [ ] `_SEL` selection screen;
- [ ] `_MAI` initialization, validations, and events;
- [ ] `_F01`/`_F0n` subroutines;
- [ ] `_CLA` class implementation;
- [ ] `_O01` PBO;
- [ ] `_I01` PAI.

## K. UI / Dynpro

- [ ] texts use the specified uppercase/lowercase conventions;
- [ ] text symbols in `WRITE`;
- [ ] dynpro/status/title numbered 0100/0200/... and associated;
- [ ] dynpro elements use TF/PF/CB/RB/PB/GB/SC/SA/TC/CC/SI prefixes;
- [ ] status includes BACK/CANCEL/EXIT;
- [ ] unused pattern sections removed.

## L. Final quality gate

- [ ] review the SLIN/extended syntax check categories described in the verification guide;
- [ ] review Code Inspector, especially performance, security, syntax/generation, and redundant code;
- [ ] list checks requiring SAP system access that cannot be completed from files alone, especially SU24/roles and actual constants API signatures.
