# ABAP - Querying constants

## When to use

Read this guide when the code:

- needs to read a business/configuration constant;
- references `ZSDTCONSTANTE`, `YBCM006`, or `ZBCCL_CONSTANTE_HANDLER`;
- uses `T_CONSTANTE`;
- contains `LOAD_CONSTANTE`, `CHECK_VALUE`, `GET_VALUE_ZVALOR`, `GET_VALUE_YVALOR`, `GET_VALUE_SINGLE`, or `GET_RANGE_REF`;
- replaces hardcoded values with configuration constants.

## Main rules

1. To query/evaluate constants registered in the constants repository, use the static class `ZBCCL_CONSTANTE_HANDLER` instead of querying the constants table directly.
2. Preload constants when initializing the ABAP object and reuse the class buffer.
3. The loading call is `ZBCCL_CONSTANTE_HANDLER=>LOAD_CONSTANTE`.
4. In programs, load constants in `INITIALIZATION`.
5. In function groups, load constants once in the `LOAD-OF-PROGRAM` event in the group header/TOP.
6. In instantiated classes, load constants in `CONSTRUCTOR`; for other designs, choose a point that guarantees a single load.
7. Check `SY-SUBRC` after `LOAD_CONSTANTE` and handle errors.
8. Loading by application ID is cumulative within the session.
9. After loading, you may query `T_CONSTANTE` or use the documented public methods.

## Clarification about LOAD_OF_PROGRAM

The class method for loading constants is `LOAD_CONSTANTE`. `LOAD-OF-PROGRAM` is the ABAP event used to preload constants in a function group.

Therefore:

- **do not generate** a call to `ZBCCL_CONSTANTE_HANDLER=>LOAD_OF_PROGRAM`;
- use `LOAD_CONSTANTE` in the appropriate lifecycle event.

## Workflow

1. Read [lifecycle-and-buffer.md](lifecycle-and-buffer.md) to decide where to load constants.
2. Read [methods.md](methods.md) to choose the correct operation.
3. Read [code-examples.md](code-examples.md) when implementing or reviewing the implementation patterns.
4. Before writing method calls, follow the actual interface installed in SAP; do not invent parameters.
