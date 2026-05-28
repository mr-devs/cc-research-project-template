---
description: Create the machine-specific data/ symlink pointing to the user's Google Drive folder for this project. Run this once per machine after cloning the repository.
---

# Task

You are a setup assistant helping a collaborator create the `data/` symlink for this project. Data is not stored in Git — it lives in a shared Google Drive folder, and each collaborator's local `data/` is a symlink to their copy of that folder on their machine.

## Instructions

### Step 1: Ask for the Google Drive path

Use **AskUserQuestion** to ask for the absolute path to the project's Google Drive folder on this machine.

Suggested question: *"Where is this project's data folder on your machine? It should be the Google Drive Desktop folder named after this repository, inside `Project Data`."*

Options to offer:
- `~/Google Drive/My Drive/Project Data/<repo-name>` — default path; replace `<repo-name>` with the project folder name (e.g. `health-search-audit`)
- Other — user types their own absolute path

### Step 2: Ask for the symlink name

Use **AskUserQuestion** to confirm which name the symlink should have at the repo root. This is almost always `data`.

Suggested question: *"What should the symlink be named at the repository root?"*

Options to offer:
- `data` — standard name used by all project scripts
- Other — user types a custom name

### Step 3: Validate

**3a. Resolve the path** — expand `~` to the full absolute path (e.g. via `echo ~`).

**3b. Check the Google Drive target exists** — run `ls "<resolved_drive_path>"`.
- If it does **not exist**, use **AskUserQuestion** to ask whether to create it now (`mkdir -p`) or abort so the user can sync the correct folder first.

**3c. Check whether the symlink name already exists at the repo root.**
- **Does not exist** — continue to Step 4.
- **Is a symlink** — show where it currently points (`readlink`), then use **AskUserQuestion** to ask whether to replace it or abort.
- **Is a real directory** — this is the expected case on a fresh clone. Use **AskUserQuestion** to ask: *"A `data/` directory already exists in the repo. Move its contents to your Google Drive folder and replace it with the symlink?"*
  - **Move and create symlink** — proceed with the steps below. If the Drive target already contains files, warn the user before continuing so they know a merge will occur.
  - **Abort** — stop so the user can handle it manually.

  If the user confirms the move:
  1. Copy the **contents** of `data/` directly into the Drive folder — the Drive folder should end up containing `raw/`, `processed/`, etc. at its top level, not a nested `data/` subdirectory. Use the trailing `/.` to copy contents rather than the directory itself:
     ```bash
     cp -R data/. "<resolved_drive_path>/"
     ```
     > ⚠️ Do **not** use `cp -R data "<resolved_drive_path>/"` — that creates an incorrect nested `data/` subdirectory inside the Drive folder.
  2. Verify the copy: compare file counts with `find data -type f | wc -l` vs `find "<resolved_drive_path>" -type f | wc -l`.
  3. Only after counts match, remove the local directory: `rm -rf data`.

### Step 4: Create the symlink

```bash
ln -s "<resolved_drive_path>" "<symlink_name>"
```

Always quote both paths to handle spaces in the Google Drive path.

### Step 5: Verify

1. Run `ls -la <symlink_name>` and confirm the `->` target is correct.
2. Run `ls <symlink_name>/` to confirm the symlink resolves and data is accessible.
3. Report success, noting that the symlink is gitignored and will not appear in `git status` — this is expected.
