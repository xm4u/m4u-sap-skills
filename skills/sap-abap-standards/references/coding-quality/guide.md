# ABAP - Code quality

## When to use

Read this guide when writing, fixing, or reviewing ABAP code. Repository object naming and HANA performance are covered in greater depth by their respective guides.

## Workflow

1. Read [coding-quality.md](coding-quality.md).
2. If the code uses `FOR ALL ENTRIES`, ranges, division/multiplication, or risky statements, pay particular attention to the critical statements section.
3. If the user requests a quality gate, audit, or final validation, read [verification.md](verification.md).
4. Apply the consolidated policy in [coding-quality.md](coding-quality.md); do not reintroduce practices that contradict these criteria.

## Review priorities

- explicit prohibitions;
- typing and data structures;
- readability/modularity;
- texts/messages/comments;
- safeguards for critical statements;
- removal of unjustified dead code.
