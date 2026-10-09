# m4u SAP Skills

A collection of SAP skills for coding agents. `sap-abap-standards` provides conventions for developing and reviewing ABAP code. `sap-gui-scripting` provides automation and testing workflows for SAP GUI for Java using its built-in JavaScript engine.

It is intended for ABAP developers, GUI testers, and coding agents working with SAP objects and desktop workflows.

## Contents

| Skill | Coverage |
| --- | --- |
| [sap-abap-standards](skills/sap-abap-standards/SKILL.md) | ABAP naming, traceability, code quality, performance, constants, authorizations, and program structure. |
| [sap-gui-scripting](skills/sap-gui-scripting/SKILL.md) | SAP GUI for Java session inspection, JavaScript automation, transaction navigation, and GUI testing on macOS, Linux, and Windows. |

The ABAP skill is organized into ten topics. Its [SKILL.md](skills/sap-abap-standards/SKILL.md) routes tasks to topic guides, detailed rules, examples, and checklists.

| Topic | Coverage |
| --- | --- |
| [Cross-cutting standards](skills/sap-abap-standards/references/core/guide.md) | Transport requests, technical headers, change markers, comments, temporary objects, and internal naming. |
| [Object naming](skills/sap-abap-standards/references/object-naming/guide.md) | Packages, programs, transactions, includes, DDIC, classes, functions, enhancements, OData, and other customer objects. |
| [Code quality](skills/sap-abap-standards/references/coding-quality/guide.md) | Declarations, internal tables, hardcoded values, FORMs, messages, texts, dead code, and critical statements. |
| [Performance](skills/sap-abap-standards/references/performance/guide.md) | Database access, SQL, HANA, indexes, internal tables, and bulk operations. |
| [Querying constants](skills/sap-abap-standards/references/constants/guide.md) | Preloading, buffering, and `ZBCCL_CONSTANTE_HANDLER` methods, with patterns for programs, function groups, and classes. |
| [Authorizations](skills/sap-abap-standards/references/authorizations/guide.md) | `AUTHORITY-CHECK`, activity-specific checks, SU24, and maintenance view access through `S_TABU_NAM`. |
| [Modularization](skills/sap-abap-standards/references/modularization/guide.md) | Routine responsibilities, parameter passing, global variables, and reuse. |
| [Program structure](skills/sap-abap-standards/references/program-structure/guide.md) | Main program and `_TOP`, `_SEL`, `_MAI`, `_F0n`, `_CLA`, `_O01`, and `_I01` includes. |
| [Formatting and screens](skills/sap-abap-standards/references/format-ui/guide.md) | Classic lists, selection texts, dynpros, titles, GUI statuses, and editor patterns. |
| [Comprehensive review](skills/sap-abap-standards/references/review/guide.md) | Topic-based checklist and findings with evidence, applicable rule, and correction. |

```text
m4u-sap-skills/
├── README.md
└── skills/
    ├── sap-abap-standards/
    │   ├── SKILL.md
    │   └── references/
    │       ├── core/
    │       ├── object-naming/
    │       ├── coding-quality/
    │       ├── performance/
    │       ├── constants/
    │       ├── authorizations/
    │       ├── modularization/
    │       ├── program-structure/
    │       ├── format-ui/
    │       └── review/
    └── sap-gui-scripting/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        └── scripts/
            ├── inspect-session.js
            ├── se16-table-smoke.js
            └── validate-scripts.cjs
```

Each ABAP topic directory contains a `guide.md` and its detailed reference files. The GUI skill links to execution, scripting, testing, and SE16 guides. All references and scripts are installed together with their skill.

## Usage

### As documentation

Browse the files on GitHub or clone the repository:

```sh
git clone https://github.com/xm4u/m4u-sap-skills.git
cd m4u-sap-skills
```

There are no project dependencies to install or build steps to run. The instructions are written in Markdown; the ABAP snippets are examples from the reference guides. The GUI scripts execute inside SAP GUI for Java and require an authenticated session and effective scripting permissions. They are not a Node.js application or a Windows COM connector.

For a specific question, open the relevant topic guide and follow its links to the detailed references. To review a complete development, start with the [comprehensive review checklist](skills/sap-abap-standards/references/review/review-checklist.md).

### Install with the skills CLI

Install the ABAP standards skill from your project directory:

```sh
pnpm dlx skills add xm4u/m4u-sap-skills --skill sap-abap-standards
```

To install the SAP GUI for Java automation/testing skill:

```sh
pnpm dlx skills add xm4u/m4u-sap-skills --skill sap-gui-scripting
```

For global installation across projects:

```sh
pnpm dlx skills add xm4u/m4u-sap-skills --skill sap-abap-standards --global
```

The CLI lets you select the target agents. To target a specific agent, add `--agent codex` or `--agent opencode`. Use `--copy` if you prefer independent copies instead of symlinks.

List the skills available in the repository without installing:

```sh
pnpm dlx skills add xm4u/m4u-sap-skills --list
```

For a local checkout or extracted ZIP, replace `xm4u/m4u-sap-skills` with the path to that folder. For example, from this repository's root:

```sh
pnpm dlx skills add . --list
pnpm dlx skills add . --skill sap-abap-standards
pnpm dlx skills add . --skill sap-gui-scripting
```

The GitHub commands require the repository and these files to be published at `xm4u/m4u-sap-skills`. Until then, use the local path commands.

See the [skills CLI documentation](https://github.com/vercel-labs/skills#options) for installation options. The skill itself has no runtime dependencies; running the CLI through `pnpm dlx` requires Node.js and pnpm.

### Manual installation from a ZIP

1. Open the [GitHub repository](https://github.com/xm4u/m4u-sap-skills), choose **Code → Download ZIP**, and extract the archive.
2. Open the extracted repository's `skills/` directory and copy the complete skill folder (`sap-abap-standards/` or `sap-gui-scripting/`) into your agent's global or project skills directory, using one of the paths below.
3. Confirm that `SKILL.md` is directly inside the installed skill folder and keep all accompanying resources together.
4. Start a new agent session. If the skill does not appear, restart the agent and check the destination path.

Choose global installation to use the skill across projects, or project installation to keep it within one project.

| Agent | Global destination | Project destination |
| --- | --- | --- |
| Codex | `~/.agents/skills/sap-abap-standards/` | `<project>/.agents/skills/sap-abap-standards/` |
| OpenCode | `~/.config/opencode/skills/sap-abap-standards/` | `<project>/.opencode/skills/sap-abap-standards/` |

For the GUI skill, replace the last path component with `sap-gui-scripting/`.

These locations are documented in the [Codex skill guide](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [OpenCode skill guide](https://docs.opencode.ai/docs/skills/#place-files). For other agents, use the skills directory documented by that agent. `~` means your home directory; on Windows, use your user profile directory for the equivalent path.

Example layout for a project using Codex:

```text
<project>/
└── .agents/
    └── skills/
        └── sap-abap-standards/
            ├── SKILL.md
            └── references/
```

Copy the skill folder itself, not the entire extracted repository or just `SKILL.md`. Keep all reference files together. No package manager or installer is required.

To update, download the latest ZIP and replace the installed skill folder with the new copy. To uninstall, remove that folder from the chosen skills directory.

### With a coding agent

You can also work from this repository and ask the agent to read the relevant files before proposing changes. For example:

```text
Review this program and its includes using sap-abap-standards and its review guide.
Consult the references for each relevant topic and report findings
with location, evidence, violated rule, and suggested correction.
Separate code checks from pending SAP system checks.
```

```text
Check the names of this program, its transaction, and its DDIC objects
using sap-abap-standards and its object naming guide. Use the reference tables to interpret module
and type codes. Do not assume a sequence number is available.
```

```text
Review constants access using sap-abap-standards and its constants guide.
Check where constants are preloaded, how the buffer is reused,
and how errors are handled. Identify signatures to confirm in SAP.
```

The comprehensive review is an entry point: it identifies the objects involved and points to the relevant topic guides. For smaller tasks, consult the affected topic directly.

### SAP GUI for Java automation and testing

Start with [setup and execution](skills/sap-gui-scripting/references/setup-and-runtime.md). Load [inspect-session.js](skills/sap-gui-scripting/scripts/inspect-session.js) in SAP GUI's scripting window and replay it to inspect reachable sessions. It reads metadata without navigating or retrieving table rows.

For the [SE16 example](skills/sap-gui-scripting/references/se16-example.md), configure a local copy of [se16-table-smoke.js](skills/sap-gui-scripting/scripts/se16-table-smoke.js) with the observed system, client, user, and optional session ID. It opens the VBAK selection screen by default; enable its execution option only for a requested table read. The example caps results at ten rows and does not modify records.

```text
Use sap-gui-scripting to inspect my open SAP GUI for Java session,
then run an SE16/VBAK display smoke test limited to ten rows.
Verify the final SAP screen and report what actually passed.
```

Scripts run in the Java client on the target desktop, not in a standalone JavaScript runtime. The initial live baseline is macOS with SAP GUI for Java 8.10 rev13; other platforms and screen variants need separate validation. Windows COM/VBScript/Python automation is outside this skill's execution adapter.

## Quick references

- **Transports and traceability:** [transport descriptions, headers, and change markers](skills/sap-abap-standards/references/core/transversal-standards.md).
- **Variables and parameters:** [internal naming conventions](skills/sap-abap-standards/references/core/internal-naming.md).
- **SAP objects:** [naming rules](skills/sap-abap-standards/references/object-naming/object-naming.md) and [module, type, and suffix tables](skills/sap-abap-standards/references/object-naming/annex-tables.md).
- **Declarations and critical statements:** [code quality](skills/sap-abap-standards/references/coding-quality/coding-quality.md).
- **SQL and internal tables:** [database and HANA](skills/sap-abap-standards/references/performance/database-hana.md) and [in-memory operations](skills/sap-abap-standards/references/performance/internal-memory.md).
- **Configuration constants:** [lifecycle and buffer](skills/sap-abap-standards/references/constants/lifecycle-and-buffer.md), [methods](skills/sap-abap-standards/references/constants/methods.md), and [ABAP examples](skills/sap-abap-standards/references/constants/code-examples.md).
- **Security:** [program authorizations](skills/sap-abap-standards/references/authorizations/program-transactions.md) and [maintenance views and SU24](skills/sap-abap-standards/references/authorizations/maintenance-views-su24.md).
- **Final verification:** [SLIN and Code Inspector](skills/sap-abap-standards/references/coding-quality/verification.md).

## Applying the rules

The skill captures the operational rules used by this repository. Keep these decisions in mind:

- `TABLES` and `OCCURS` are prohibited under this package's criteria. Tables and parameters must be explicitly defined and typed.
- `DEFAULT` on selection screens and `INTO CORRESPONDING FIELDS` are permitted in the cases described; their presence alone is not a violation.
- `FOR ALL ENTRIES` is permitted, but the driver table must be checked for entries before use.
- Constants are loaded with `LOAD_CONSTANTE`. `LOAD-OF-PROGRAM` is the ABAP event used in function groups, not a class method.
- The modular structure is required for new programs with events or more than 500 lines. Includes are added according to the content needed.

Detailed rules and their conditions are in each topic's references. External recommendations must be identified as such when proposed alongside this repository's standard.

## Review scope

Files allow checks of naming, structure, declarations, queries, authorization logic, and code traceability. A complete review also requires access to the SAP system for SU24 and role configuration, sequence number availability, existing objects, and actual class signatures.

The review guide ranks findings as `Critical`, `High`, `Medium`, or `Low`, and asks for location, evidence, the standard's requirement, and a correction. Checks that cannot be performed must be listed as pending, with enough context to resolve them.

Reference examples explain the patterns. Before incorporating them into a development, adapt them to the objects, types, and interfaces available in the system.

## Changing the rules

When proposing a correction, identify the affected reference and the rule or evidence supporting it. If a shared criterion changes, also update the review checklist and dependent examples to avoid contradictory instructions.
