# General formatting recommendations

## 5.1 Comments

- every program must include comments;
- keep comments clear and concise;
- use lowercase according to the general rule;
- describe the section's purpose.

## 5.2 FORM subroutines

Use them to:

- encapsulate complex/long code;
- improve readability and maintenance;
- define processes called from different places only once.

Formatting rules:

- average length no greater than one page of code;
- FORM and parameter names must follow the internal convention;
- include comments describing functionality and input/output parameters.

## 5.3 Classic list headers

For `WRITE` reports, the header must contain:

1. company name (`T001-BUKRS` as specified by this rule);
2. report title in uppercase;
3. issue date in `DD/MM/YYYY` format;
4. report name (`SY-REPID`);
5. optional subtitle in uppercase;
6. page number;
7. column headers in uppercase.

These details must appear whether standard text elements are used or the header is built in `TOP-OF-PAGE`.

## 5.4 Selection texts

Texts for `PARAMETERS` and `SELECT-OPTIONS` must be written in lowercase.

## 5.5 Text symbols

Text symbols may use lowercase or uppercase depending on their display location and the applicable rules. They must be used in `WRITE` statements to avoid embedded literals.

## 5.6 Screens

Follow SAP style:

- lowercase field texts;
- use DDIC references;
- use frames for related fields;
- order fields to make data entry easier.

## 5.7 Dynpros, statuses, and titles

Use consecutive 4-digit numbering in increments of 100:

```text
0100, 0200, 0300, ...
```

Keep the dynpro, status, and title associated through the same number.

If a dynpro reuses another dynpro's status, its unused status number must remain available so that it can have its own status later.

### Dynpro elements

| Element | Prefix |
|---|---|
| Text field | `TF_` |
| Input/output | `PF_` |
| CheckBox | `CB_` |
| Radio Button | `RB_` |
| PushButton | `PB_` |
| Frame | `GB_` |
| TabStrip | `SC_` |
| Subscreen Area | `SA_` |
| Table Control | `TC_` |
| Custom Control | `CC_` |
| Status Icon | `SI_` |

If the element references DDIC or a program variable, keep the name assigned automatically by that reference.

## 5.8 GUI status

- use SAP defaults for functions and menus wherever possible;
- use lowercase interface titles matching the interface name;
- every interface must include `BACK`, `CANCEL`, and `EXIT`;
- use lowercase text for custom pushbuttons.

## 5.9 Patterns

Patterns defined in these references:

- `PAT_GEN`: general program structure;
- `PAT_TOP`: global declarations;
- `PAT_SEL`: selection parameters;
- `PAT_MAI`: main program validations and events.

Unused pattern sections must be removed, not left commented out.
