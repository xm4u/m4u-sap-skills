# Testing and evidence

## Choose what to prove

Define the test's starting state, target system/client/user, transaction, screen/control assertions, data fixture or filters, expected result, and finish state. Preserve the user's requested scope. A navigation smoke test and a business data test prove different things.

Useful layers:

| Layer | Observable proof |
| --- | --- |
| Local validation | Script syntax and meaningful fixture behavior; no live SAP claim |
| Runtime access | Inspection JSON lists the intended authenticated session without errors |
| Navigation | Returned transaction/program/dynpro plus the visible destination screen |
| Display/query | The requested table's selection screen or bounded results, as specified |
| Business workflow | Expected business state or persisted result, with an authorized fixture |
| Regression | Same defined case repeated across relevant versions/screens/platforms |

Do not treat an accepted script, a success status message, or a screenshot alone as proof of every layer. For a table query, distinguish opening the table selector, opening its selection screen, and displaying rows. Zero rows can be a valid query result but cannot pass a case that requires a known record.

## Execute a case

1. Inspect the session using Java's `java-shell.py --script scripts/inspect-session.js` (or the editor when no bridge is loaded), or Windows' `inspect-session.vbs`. Account for inventory errors and effective read-only/recording restrictions.
2. Configure a local Java script copy or Windows named arguments with the observed identity and exact IDs. If several sessions match, select the observed session ID as well. Keep personal settings outside the reusable skill.
3. Confirm the starting screen has no unrelated unsaved work or unresolved popup. Navigation authorization does not imply authorization to save, post, delete, export, or change roles.
4. Run once; wait for Java shell JSON/exit code, editor **RECEIVED**, Windows JSON/exit code, or an exception. Check screen identity at each transition through scripting; inspect the final native UI when available. Without desktop tools, assert the final controls, title, status and relevant results explicitly and report visual checks as unperformed.
5. If the action fails, record the actual failing phase, error/status message, and observed state. Resume from that state only after understanding it; do not rerun the entire workflow blindly.
6. Leave the requested final screen visible unless the user asked to restore the starting state. Do not log out or close unrelated sessions as cleanup.

## Assertions

Use system/client/user matches and exact expected technical values where available. Use control IDs and values for fields; use localized titles as supporting evidence, not the sole selector. For data tests specify a known key/filter and expected row condition. For large tables, a small row cap is appropriate for a basic display smoke test; correctness assertions need a deterministic fixture.

For screenshot/UI assertions include the active transaction/table name and the relevant control/result region. Avoid committing full-screen images of real business data. Capture only evidence needed for the test, redact it before sharing, and keep raw output local.

Use `PASS`, `FAIL`, and `BLOCKED` accurately: missing access or an unavailable runtime is blocked; an unmet assertion is failed; an executed, observed expected result is passed. Do not mark missing live checks as passed because mocks succeeded.

## Result format

Report case, client version/platform, starting state, executed actions, assertions and observed results, final state, and untested limits. Use anonymized target identity in committed examples. Keep any business changes and cleanup outcomes explicit when the requested test includes them.

When adding reusable scripts, validate missing host objects, absent/multiple session matches, read-only mode, unexpected popups, and success/error paths with local fixtures. These checks protect selection and stopping behavior; they do not replace live SAP execution.

The optional [local validator](../scripts/validate-scripts.cjs) exercises the bundled scripts against fixtures and requires Node.js, with no additional packages:

```sh
pnpm exec node skills/sap-gui-scripting/scripts/validate-scripts.cjs
```

Run that command from this repository's root. For an installed/copied skill, pass its actual script path instead. It never attaches to SAP or changes a desktop. The Node requirement applies only to these development checks, not to executing `.js` files in the Java client.

Also run `python3 skills/sap-gui-scripting/scripts/validate-java-shell.py` for the Java shell protocol. It checks transport failures and uncertain-outcome lock preservation locally, without SAP. Read [Java shell execution](java-shell-runtime.md) for the separate live baseline.

For Windows COM selection and stopping behavior, also run [Windows VBS fixtures](../scripts/windows/validate-scripts.vbs):

```powershell
cscript.exe //nologo skills/sap-gui-scripting/scripts/windows/validate-scripts.vbs
```

These fixtures use COM-shaped mocks in VBScript; they do not attach to SAP or prove live table access. They check argument validation, inventory, session selection, and stopping before navigation. The separate live baselines are recorded in [SE16 evidence](se16-example.md).
