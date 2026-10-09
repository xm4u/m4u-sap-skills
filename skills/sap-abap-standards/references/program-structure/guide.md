# ABAP - Program structure

## Applicability rule

Every new program that has events or more than 500 lines must use this modular structure as its baseline.

## Workflow

1. Read [program-control-top-sel.md](program-control-top-sel.md) for the main program, `_TOP`, and `_SEL`.
2. Read [mai-and-events.md](mai-and-events.md) for `_MAI`.
3. Read [f01-cla-pbo-pai.md](f01-cla-pbo-pai.md) for `_F0n`, `_CLA`, `_O01`, and `_I01`.
4. Keep include names tied to the main program's name.
5. Do not mix content between includes without explaining why.
