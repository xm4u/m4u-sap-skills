# Dynamic memory / internal table performance

## Searching STANDARD TABLE

For repeated searches or large volumes, keep the table sorted by the key and use:

```abap
READ TABLE ... WITH KEY ... BINARY SEARCH.
```

## Select once, reuse in memory

When searching the same data repeatedly, select it once and work with an internal table.

## SORT

- specify fields with `BY`;
- specify `ASCENDING` / `DESCENDING` where applicable;
- avoid accidentally sorting by all fields.

## LOOP ... WHERE

Prefer `LOOP ... WHERE` over `LOOP` + `CHECK`, as the condition is evaluated internally.

## Cleanup

Using `CLEAR` / `REFRESH` after a loop is recommended when the data will not be reused.

## Copying tables

If two tables have the same structure:

- copy directly (`GT_AUX[] = GT_VBAK[]`) instead of using a loop + append;
- use `APPEND LINES OF` if the target already contains data that must not be overwritten.

## Partial MODIFY

If only one field changes, use `TRANSPORTING <field>` to limit the modification.

## Duplicates

Sort and use `DELETE ADJACENT DUPLICATES` instead of manually deleting within a loop.

## Counting rows

Avoid a loop to count records. `DESCRIBE TABLE ... LINES` is suggested.

## Nested SELECT statements

Avoid SELECT statements inside loops when the volume can grow. Prefer preloading, for example with `FOR ALL ENTRIES`.

## Nested loops over large tables

When two tables share a key, a start-index technique (`FROM LI_INDX`) may be used to avoid scanning the second table from the beginning on every iteration.

## Array operations

Prefer bulk operations:

```abap
INSERT <dbtab> FROM TABLE <itab>.
```

over individual `INSERT` statements inside a `LOOP`.

## Large datasets: two strategies

1. Preload with `FOR ALL ENTRIES` before the main loop.
2. In-memory buffer table: search the buffer first and query the database only if the entry is absent; add both the found value and the queried key to the buffer to avoid repeated access.
