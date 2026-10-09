# Quality assurance - Coding and presentation

## 2.1.1 Variable handling

Key rules:

- use `TYPE`, not `LIKE`, to reference Dictionary types;
- specify variable lengths where applicable;
- method parameters must be typed; if the type is unknown, use `TYPE ANY`;
- do not pass system fields directly as parameters: pass them through a variable;
- `TABLES` is prohibited throughout the code under this operational standard; do not use `TABLES` declarations or parameters; use work areas and typed parameters through `USING`/`CHANGING` or `IMPORTING`/`EXPORTING`/`CHANGING` interfaces, as appropriate;
- field symbols must have an assignment type; in ABAP Objects, `TYPE` is mandatory;
- do not use `RANGES`; use `DATA ... TYPE RANGE OF`;
- `OCCURS` is completely prohibited; use `INITIAL SIZE` if initial memory allocation is required;
- when using `LOOP ... INTO <work area>`, clear the work area, not the internal table;
- do not use implicit internal table header lines; use work areas or field symbols;
- for database operations, use explicit work areas instead of implicit header lines.

## 2.1.2 Inline declarations

Inline forms are accepted, for example:

```abap
DATA(lv_name) = 'TEXT_INLINE'.
LOOP AT lt_mara INTO DATA(lw_mara).
READ TABLE lt_mara INTO DATA(lw_mara) INDEX 1.
SELECT ... INTO TABLE @DATA(lt_mara) ...
```

`VALUE` and `LET` are also illustrated by this standard.

## 2.1.3 Internal tables

Rules:

- always use tables without header lines;
- never use `OCCURS` or `TABLES`; explicitly define typed internal tables and structures;
- do not use `RANGES`; use `TYPE RANGE OF`;
- specify the table type: `STANDARD`, `SORTED`, or `HASHED`;
- specify the primary key or `WITH EMPTY KEY`.

### STANDARD TABLE

Suitable when:

- access by index or key is needed;
- the key is non-unique;
- the same program uses multiple access keys;
- key-based table expressions are not used;
- no more specific alternative applies.

Considerations:

- do not use `WITH DEFAULT KEY`; use `WITH EMPTY KEY`, an explicit key, or `WITH KEY table_line`;
- for key access, sort by that key and use `BINARY SEARCH` in `READ TABLE`.

### SORTED TABLE

Suitable when:

- access by index or key is needed;
- the key may be unique or non-unique;
- partial keys are used;
- nested loops exist.

Specify the primary key. In `READ TABLE ... WITH TABLE KEY`, follow the field order defined by the key.

### HASHED TABLE

Suitable when:

- access uses the complete key;
- constant access time is desired;
- a unique key can be defined and the volume is large.

Index access is unavailable. The key is `UNIQUE` and must be specified.

## 2.1.4 Hardcoded values

Do not hardcode business values in source code, as this makes maintenance, portability, and reuse more difficult.

Alternatives:

- selection parameters;
- constants table;
- if unavoidable, a global constant.

Exception: single-use conversion programs.

## 2.1.5 Events

- order events by their execution sequence where possible;
- remove unused events;
- place FORMs after the main code in a FORM include;
- order FORMs by their call sequence where possible.

## 2.1.6 Subroutines (FORM)

- use a descriptive name: infinitive verb + object (`find_supplier`, `save_order`, `calculate_invoice_vat`);
- include a header with a brief description and input/output parameters;
- keep one main process per subroutine; split routines containing several;
- move a routine into a function module if it can be reused by other programs;
- use `USING` for inputs; pass by value with `VALUE(...)` where applicable;
- use `CHANGING` for outputs.

## 2.1.7 Nesting

Avoid excessively long blocks and deep nesting in `IF`, `LOOP`, `CASE`, `DO`, etc. Balance the structure through subroutines, taking cohesion and coupling into account.

## 2.1.8 Statements

- start each statement on a new line;
- indent levels by 2 spaces;
- Pretty Printer may be used;
- split long statements across multiple lines and indent consistently.

## 2.1.9 Grouping global variables

Related variables must be grouped as fields of a structure rather than separate variables.

## 2.1.10 Assignments

Criteria:

- avoid `MOVE-CORRESPONDING` by default and prefer explicit assignments (`MOVE` or `=`); `MOVE-CORRESPONDING` is permitted only when field-by-field mapping would make transfers between compatible work areas/structures disproportionately complex;
- use `TYPE` instead of `LIKE` for data definitions;
- `OCCURS` is prohibited in all forms, and `WITH HEADER LINE` should be avoided; use work areas or field symbols.

## 2.1.11 Messages

All error messages must use `MESSAGE ID` / message classes, not literals with `WRITE`.

## 2.1.12 Parameters / Selection screen

- `DEFAULT` is permitted in `PARAMETERS` and other selection screen fields when it provides a useful initial value; it must not be reported as a violation on its own;
- add search help where useful;
- group related parameters in `BLOCKS`/frames;
- replace the default generated name with descriptive selection text.

## 2.1.13 Text literals

Use `TEXT ELEMENTS` for program texts instead of embedded literals.

## 2.1.14 Dead code

- do not leave unjustified dead code;
- explain the reason if it must remain;
- when modifying the original code, this standard requires keeping replaced/corrected code commented out with its change marker.

## 2.1.15 Comments

- the entire program must include useful comments;
- explain and clarify the logic instead of mechanically describing each statement;
- write comments in lowercase; a sentence may begin with an uppercase letter;
- keep the level of commenting consistent throughout the program;
- add comments during development, not just at the end.

## 2.1.16 Declaration comments

Comment declared variables on the right using `"` to describe the data.

Conceptual example:

```abap
DATA gi_lines TYPE i. " number of records found
```

## 2.1.17 WRITE for numeric values

When a numeric field has decimals, specify them using the appropriate format and include the currency if it is an amount.

## 2.1.18 Structures

Do not use legacy definitions based on `INCLUDE STRUCTURE` + `OCCURS`; `OCCURS` is prohibited. Define the type and internal table explicitly.

## 2.1.19 Critical statements

### FOR ALL ENTRIES

Before use, check that the driver table has entries. Risk: full scan and possible timeout.

### Empty ranges

Before `WHERE field IN range`, check that the range is not empty when an empty range could trigger mass reads.

### Arithmetic operations

Division and multiplication must be validated or protected by exception handling to prevent, among others:

- `CX_SY_ZERODIVIDE`
- `CX_SY_ARITHMETIC_OVERFLOW`
