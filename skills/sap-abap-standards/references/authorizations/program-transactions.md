# Authorization in program transactions

## General rule

Every ABAP program must check one or more authorization objects. The check must restrict the information displayed or processed according to the user's authorization and activity.

The standard provides two levels of control:

- organizational level;
- as a fallback, the level of the tables/information accessed.

## Activity-specific checks

When an application supports more than one activity, a single generic check is insufficient.

Examples of functional activities:

- create;
- change;
- display;
- delete;
- print;
- post.

The check must run at the specific action. For example, create authorization must be checked in the routine associated with the **Create** button.

`ACTVT` values covered by this guide:

| Activity | ACTVT |
|---|---:|
| Create | `01` |
| Change | `02` |
| Display | `03` |

For other activities, do not infer or invent the code: check the authorization object/SU24 in the system.

## Implementation pattern

Example of a check in a selection event:

```abap
AT SELECTION-SCREEN.
  AUTHORITY-CHECK OBJECT 'ZMM_WERKS'
    ID 'WERKS' FIELD p_werks
    ID 'ACTVT' FIELD '03'.

  IF sy-subrc NE 0.
    MESSAGE e000 WITH text-e01 p_werks.
  ENDIF.
```

### Naming note

For this package, apply the development naming convention: customer authorization objects use `Z[MM]_[X...X]`, for example `ZMM_WERKS`.

## Check placement

- Input parameter checks may run in selection screen events.
- A specific action must check authorization immediately before the sensitive operation.
- Do not rely solely on hiding/disabling buttons: the check must exist in the logic that executes the action.
- Evaluate `SY-SUBRC` immediately after `AUTHORITY-CHECK`.
- On failure, do not continue with unauthorized reads/processing/updates.

## SU24

The transaction must be registered in `SU24` with its authorization object, proposed values, and corresponding activities.

Example transaction configuration:

- `S_TCODE` for transaction checks;
- a customer organizational object (for example, `ZMM_WERKS`);
- `ACTVT` with `01`, `02`, `03`;
- the organizational field `WERKS`.

Maintaining the transaction and its authorization object in SU24 is an explicit requirement of this standard.

## Code checklist

- [ ] `AUTHORITY-CHECK` exists when the program processes information subject to access restrictions.
- [ ] The object matches the program's module/scope.
- [ ] Check IDs correspond to fields in the object.
- [ ] `ACTVT` represents the action being executed.
- [ ] `SY-SUBRC` is evaluated immediately.
- [ ] Failure stops/blocks the operation.
- [ ] Each action has its own specific check when multiple actions exist.
- [ ] SU24 verification is listed as a pending system check when SAP access is unavailable.
