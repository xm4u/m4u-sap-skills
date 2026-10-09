# Modularization and reuse

## 2.3.1 Modularization

Programs must be fully modularized.

Principles:

- the main program summarizes the main processes through modules/subroutines;
- each subroutine is divided coherently into subprocesses when needed;
- modularization is designed from the start;
- each module or routine performs **one main action**;
- dividing a large problem into smaller ones makes understanding, tracking, and maintenance easier;
- good modularization and parameterization support reuse.

Conceptual example:

```abap
START-OF-SELECTION.
  PERFORM find_data.
  PERFORM calculate_percentages.
  PERFORM save_log.
END-OF-SELECTION.
  PERFORM print_report.
  PERFORM download_file.
```

## 2.3.2 Module parameterization

- declare global variables only when justified;
- do not declare a variable global if it is used only within one module;
- pass parameters between modules through `USING` and `CHANGING`; `TABLES` is prohibited;
- even when a global variable is technically accessible, passing it as a parameter can clarify whether the module reads or changes it.

## 2.3.3 Structural balance

Modules at the same level must have similar functional abstraction levels.

Conceptually incorrect:

```text
load_data
print_header
print_detail
```

when the last two are subprocesses of the same activity.

Better:

```text
load_data
print_data
  -> print_header
  -> print_detail
```

## 2.3.4 Reuse

Identify reusable components during design.

Reuse options:

- reusable types -> `TYPE-POOLS`;
- reusable definitions -> `INCLUDES`;
- reusable FORMs -> routine pools or includes;
- reusable FORMs with input/output parameters -> function modules.

Conditions for reuse:

- do not carry over performance or coding defects;
- avoid hardcoded values;
- modularize;
- parameterize;
- keep the code presentation readable and orderly.
