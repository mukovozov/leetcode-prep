# leetcode-prep

LeetCode interview redo-list tracker.

## How it works

- **`redo.json`** is the source of truth — a machine-readable list of problems to redo.
- **`redo.md`** is auto-generated from `redo.json` on every mutation. Never edit it by hand.
- **`redo.py`** is the CLI that keeps both files in sync and auto-pushes.

## CLI usage

```bash
# Add a problem
python3 redo.py add 75 "Sort Colors" --pattern two-pointers --reason slow --target 15 --notes "missed mid advance"

# Mark as cleared
python3 redo.py done 75

# Reopen
python3 redo.py reopen 75

# List (all or open only)
python3 redo.py list
python3 redo.py list --open

# Skip auto-push on any mutation
python3 redo.py add 75 "Sort Colors" --pattern two-pointers --reason slow --target 15 --no-push
```

## Raw JSON URL

```
https://raw.githubusercontent.com/mukovozov/leetcode-prep/main/redo.json
```
