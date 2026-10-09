---
name: sap-abap-standards
description: Develop, modify, and review ABAP code and SAP customer objects using the naming, traceability, quality, performance, constants, authorization, and program structure conventions in this skill. Use for ABAP implementation tasks or reviews against these conventions.
---

# SAP ABAP standards

Use this skill for ABAP implementation, maintenance, naming checks, and reviews against the bundled conventions.

## Workflow

1. Identify the task and the affected SAP artifacts: programs, includes, classes, function groups, DDIC objects, transactions, maintenance views, dynpros, or services.
2. For implementation or changes, read the cross-cutting and code quality guides, then the topic guides relevant to the affected objects. For a review, start with the review guide and its checklist.
3. Follow each guide's links to the detailed references needed for the task. Read only applicable topics; do not load the entire reference library by default.
4. Apply the rules to the requested scope and explain any required corrections. Separate code-level findings from checks that need access to the SAP system.

All topic guides and supporting files below are part of this single skill; no separate skills are required.

## Topic routing

| Task or artifact | Guide |
| --- | --- |
| Technical headers, change markers, transport requests, temporary objects, or internal naming | [Cross-cutting standards](references/core/guide.md) |
| Creating, renaming, or checking Y/Z repository objects, including DDIC and OData names | [Object naming](references/object-naming/guide.md) |
| Writing, fixing, or reviewing declarations, internal tables, FORMs, messages, or critical statements | [Code quality](references/coding-quality/guide.md) |
| Database access, large datasets, internal table searches, HANA, CDS, or AMDP | [Performance](references/performance/guide.md) |
| Configuration constants or `ZBCCL_CONSTANTE_HANDLER` | [Querying constants](references/constants/guide.md) |
| Z transactions, sensitive activities, `AUTHORITY-CHECK`, SU24, or maintenance views | [Authorizations](references/authorizations/guide.md) |
| Splitting responsibilities, passing parameters, extracting routines, or designing reusable components | [Modularization](references/modularization/guide.md) |
| New programs with events or more than 500 lines, or changes to include organization | [Program structure](references/program-structure/guide.md) |
| Classic lists, selection screens, dynpros, GUI statuses, titles, or editor patterns | [Formatting and screens](references/format-ui/guide.md) |
| Comprehensive development reviews or compliance audits | [Review workflow](references/review/guide.md) |

## Applying the conventions

- Use the bundled rules as this skill's operational criteria. Do not replace them with external ABAP conventions unless the user explicitly requests it. Identify external recommendations as such.
- Preserve conditions and exceptions in the detailed references. Do not flag a rule that does not apply to the object or task.
- Do not invent available sequence numbers, authorization activity codes, or method signatures. Verify them in SAP or identify them as pending checks.
- Keep the installed constants interfaces unchanged: use `ZBCCL_CONSTANTE_HANDLER` and `LOAD_CONSTANTE`; `LOAD-OF-PROGRAM` is an ABAP event, not a class method.

For a requested review, use the findings format and severity levels in the [review guide](references/review/guide.md). For implementation work, explain the applicable rules and any SAP checks that remain pending.
