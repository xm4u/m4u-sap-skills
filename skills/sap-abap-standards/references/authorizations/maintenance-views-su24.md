# Maintenance views and SU24

## Rule

For a maintenance view/transaction, configure access control by registering the following in `SU24`:

- the transaction;
- the `S_TABU_NAM` object;
- the table accessed by the view;
- the permitted activities.

## Documented activities

| Action | ACTVT |
|---|---:|
| Create | `01` |
| Change | `02` |
| Display | `03` |

## Configuration example

An SU24 configuration for a maintenance transaction includes:

- `S_TABU_NAM` for table access through standard tools;
- `S_TCODE` for transaction start checks;
- `ACTVT` with `01`, `02`, and `03`;
- the `TABLE` field with the corresponding maintenance table.

## Agent rule

When a change affects a maintenance view:

1. identify the maintenance transaction;
2. identify the actual affected table;
3. require/propose registration of `S_TABU_NAM` in SU24;
4. assign only the activities required by the use case;
5. do not mark SU24 as "correct" just because the code compiles: this is a SAP configuration check.

## Typical findings

Report a security finding if:

- the maintenance view does not account for `S_TABU_NAM`;
- SU24 does not reference the actual table;
- broader activities than necessary are granted;
- the design relies solely on knowing the transaction, without table authorization checks.
