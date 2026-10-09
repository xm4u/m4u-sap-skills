# ABAP - Authorizations

## When to use

Read this guide when creating, modifying, or reviewing:

- a Z transaction associated with an ABAP program;
- a report/program that displays or processes information subject to access restrictions;
- create, change, display, or other sensitive activities;
- a maintenance view/transaction;
- code using `AUTHORITY-CHECK`;
- SU24 configuration or reviews.

## Mandatory rules

1. Every ABAP program must implement one or more authorization checks at the organizational level or, as a fallback, at the level of the tables/information accessed.
2. If the program supports multiple activities, each action must be checked against its corresponding activity at the point where that action is executed.
3. Immediately evaluate `SY-SUBRC` after `AUTHORITY-CHECK` and block the operation if the user is not authorized.
4. The authorization object must match the development module and follow the naming convention defined by [object-naming guide](../object-naming/guide.md).
5. The transaction and its objects/values/activities must be registered in `SU24`.
6. For maintenance views, use `S_TABU_NAM` with the affected table and authorized activities.
7. Do not invent `ACTVT` codes that are not documented or confirmed in the system. This standard explicitly defines `01` create, `02` change, and `03` display.

## Workflow

1. Read [program-transactions.md](program-transactions.md) when ABAP code is executable through a transaction.
2. Read [maintenance-views-su24.md](maintenance-views-su24.md) for maintenance views/transactions or SU24 work.
3. If the authorization object's name is part of the change, also consult [object-naming guide](../object-naming/guide.md).
4. In reviews, distinguish code-level checks from SU24/role checks that require access to the SAP system.
