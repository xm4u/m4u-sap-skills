# ABAP - Cross-cutting standards

## When to use this guide

Use this guide when creating or modifying any ABAP object subject to this repository's standard, especially when you need to:

- prepare technical headers or change markers;
- validate a transport request/description;
- name variables, internal tables, structures, types, classes, or objects;
- create temporary/test objects;
- review comments and change traceability.

## Workflow

1. Read [transversal-standards.md](transversal-standards.md).
2. If the task mainly concerns internal names, also consult [internal-naming.md](internal-naming.md).
3. Do not modernize or replace the rules with external ABAP conventions unless the user explicitly requests it.
4. Apply the operational rules in these references as the current project criteria.

## Expected output

When proposing or reviewing code, cite the specific rule in plain language and show the required correction. For audits, separate `Non-compliance`, `Risk/impact`, and `Suggested correction`.
