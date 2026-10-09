# Verification with SLIN and Code Inspector

SLIN and Code Inspector complement code reviews. This guide suggests check categories; it does not mandate a specific execution variant.

## Extended program check / SLIN

Extended check categories worth reviewing:

- `PERFORM/FORM` interfaces;
- `CALL FUNCTION` interfaces;
- external program interfaces;
- dynpro consistency;
- load table checks;
- authorizations;
- GUI status / title bar;
- SET/GET parameter IDs;
- `MESSAGE`;
- character strings;
- output of `CURR/QUAN` fields;
- field properties;
- syntax check warnings;
- internationalization;
- package checks;
- redundant statements;
- problematic statements;
- structure enhancements;
- obsolete statements.

Review SLIN errors, warnings, and messages by category.

## Code Inspector

Review Code Inspector results in categories such as:

- performance checks;
- security checks;
- syntax/generation checks;
- redundant code/statements.

## Recommended use

If the user requests a final review, try to cover these categories conceptually in addition to the written rules. Do not present a specific SLIN/SCI variant as mandatory unless the project has defined it.
