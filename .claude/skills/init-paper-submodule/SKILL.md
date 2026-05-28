---
name: init-paper-submodule
description: Use when the user wants to convert a project's `paper/` directory into a git submodule pointing at a separate paper repo (typically for Overleaf linking). Handles removing any existing tracked `paper/` content, adding the submodule, writing a standardized README inside the submodule, and updating the parent repo's README.
argument-hint: "[git@github.com:<owner>/<paper-repo>.git]"
---

# init-paper-submodule

Converts a project's `paper/` directory into a git submodule that points at a dedicated paper repository. Mirrors the setup used in the `llm-memory-bias` project: the main repo holds code/data/results, and `paper/` is a separately pushable submodule (useful for Overleaf linking).

## Inputs needed

Before proceeding, you need:

1. **Paper repo SSH URL** — the `git@github.com:...` URL for the paper repo (e.g., `git@github.com:mr-devs/my-project-paper.git`). This is passed as `$ARGUMENTS`. If not provided, use `AskUserQuestion` to ask the user for it before doing anything else.
2. **Project root** — the current working directory (`os.getcwd()` / `pwd`). Confirm the directory is a git repo (`.git/` exists) before proceeding. If it is not, use `AskUserQuestion` to ask the user to confirm or provide the correct path.

From the SSH URL, derive:
- `<PAPER_REPO_URL>` — the HTTPS form, e.g. `https://github.com/mr-devs/my-project-paper`
- `<PARENT_REPO_URL>` — HTTPS form of the parent repo (`git remote get-url origin`, converted from SSH if needed)
- `<PARENT_REPO_SSH_URL>` — SSH form of the parent repo (from `git remote get-url origin`)
- `<PROJECT_NAME>` — the parent repo's name (basename of the repo URL, without `.git`)

## Edge cases (check before acting)

- **`.gitmodules` already has a `paper` entry** → abort and tell the user `paper/` is already registered as a submodule.
- **`paper/` is a regular tracked directory** → proceed with `git rm -r paper` below; this is the normal case.
- **`paper/` doesn't exist** → skip the removal step; just add the submodule.
- **Remote repo already has content** → don't overwrite existing files; only add/update `README.md`.

## Procedure

### Step 1 — Remove existing tracked `paper/` (if present)

```bash
git rm -r paper
git commit -m "Remove placeholder paper/ before adding submodule"
```

Skip this step if `paper/` is not tracked (i.e., `git ls-files paper` returns nothing).

### Step 2 — Add the submodule

```bash
git submodule add <paper-repo-ssh-url> paper
```

This clones the remote into `paper/` and creates `.gitmodules`.

### Step 3 — Write the submodule README

Copy `reference-paper-readme.md` from this skill's directory (`~/.claude/skills/init-paper-submodule/reference-paper-readme.md`) into `paper/README.md`, replacing all placeholders:

| Placeholder | Replace with |
|---|---|
| `<PROJECT_NAME>` | e.g. `fact-check-diversity` |
| `<PARENT_REPO_URL>` | e.g. `https://github.com/mr-devs/fact-check-diversity` |
| `<PARENT_REPO_SSH_URL>` | e.g. `git@github.com:mr-devs/fact-check-diversity.git` |
| `<PAPER_REPO_URL>` | e.g. `https://github.com/mr-devs/fact-check-diversity-paper` |

Then commit and push **inside the submodule**:

```bash
cd paper
git add README.md
git commit -m "Add submodule-style README"
git push
cd ..
```

### Step 4 — Update the parent repo's top-level README.md

Add (or update) a `## Submodules` section near the top of `README.md`. Use this format, substituting real values for the placeholders:

```markdown
## Submodules

The [`paper/`](paper/) directory is a git submodule pointing to <PAPER_REPO_URL>. Changes inside `paper/` must be pushed separately from the parent repo. See [`paper/README.md`](paper/README.md) for setup, update, and push instructions.

To populate `paper/` after cloning this repo:

\```bash
git submodule update --init --recursive
\```

Or clone the parent with submodules in one step:

\```bash
git clone --recurse-submodules <PARENT_REPO_SSH_URL>
\```
```

Place this section before `## Contents` (or at the top of any existing sections if `## Contents` doesn't exist).

### Step 5 — Commit the parent repo

```bash
git add .gitmodules paper README.md
git commit -m "Add paper/ as git submodule"
```

Do **not** push the parent repo automatically — let the user push when ready.

## Verification

After completing all steps, run:

```bash
git submodule status           # should list one entry for paper/
cat .gitmodules                # should show the paper submodule URL
ls paper/                      # should show the remote's files + README.md
cd paper && git remote -v      # should show the supplied paper repo URL
```

Report the output of these commands to the user so they can confirm everything looks correct.
