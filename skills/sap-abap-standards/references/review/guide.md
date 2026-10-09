# Comprehensive ABAP review

## Objective

Review ABAP code and objects against this repository's criteria and procedures without loading every reference unnecessarily.

## Audit workflow

1. Identify the existing artifacts: program, includes, classes, functions, tables/DDIC, dynpros, OData, maintenance views, transactions, etc.
2. Read [review-checklist.md](review-checklist.md).
3. Read/consult topic-specific guides only when relevant:
   - traceability/internal naming -> [core guide](../core/guide.md);
   - quality -> [coding-quality guide](../coding-quality/guide.md);
   - SQL/HANA/performance -> [performance guide](../performance/guide.md);
   - configuration constants -> [constants guide](../constants/guide.md);
   - authorizations/SU24/maintenance views -> [authorizations guide](../authorizations/guide.md);
   - module design -> [modularization guide](../modularization/guide.md);
   - repository objects -> [object-naming guide](../object-naming/guide.md);
   - includes/program -> [program-structure guide](../program-structure/guide.md);
   - dynpro/formatting -> [format-ui guide](../format-ui/guide.md).
4. Do not report a rule as violated when it does not apply to that object type.
5. Use the consolidated rules in the topic-specific guides as the operational authority.
6. Clearly separate code findings from checks requiring access to the SAP system (`SU24`, roles, existing objects, actual class signatures, etc.).

## Output format

Order findings by practical severity:

- `Critical`: risk of unauthorized access, mass reads, timeout, exception, or likely functional error.
- `High`: significant structure/naming or maintainability violation with material impact.
- `Medium`: code quality/readability violation.
- `Low`: minor formatting, comment, or consistency issue.

For each finding:

```text
[Severity] Rule
Location: file / include / routine / line, if known
Evidence: minimal snippet
Standard requirement: ...
Correction: ...
```

End with a compliance summary and a list of checks that could not be verified due to missing context/SAP access.
