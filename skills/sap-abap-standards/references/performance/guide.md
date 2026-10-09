# ABAP - Performance

## When to use

Use this guide when an ABAP change reads/writes the database, handles high volumes, uses large internal tables, `FOR ALL ENTRIES`, HANA, or CDS/AMDP.

## Workflow

1. Read [database-hana.md](database-hana.md) for database/HANA access.
2. Read [internal-memory.md](internal-memory.md) when the task focuses on internal tables and loops.
3. For configuration constants or `ZBCCL_CONSTANTE_HANDLER`, read [constants guide](../constants/guide.md) rather than handling them through the performance guide.
4. Do not propose optimizations that explicitly contradict the standard without labeling them as external recommendations.
