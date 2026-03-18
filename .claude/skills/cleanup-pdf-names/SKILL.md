---
name: cleanup-pdf-names
description: Clean up PDF filenames by removing spaces, em dashes, and special characters
argument-hint: <path/to/directory>
disable-model-invocation: false
---

# Cleanup PDF Names Command

Clean up PDF filenames for filesystem compatibility and consistency.

## Input

$ARGUMENTS

## Instructions

### Step 1: Determine Target Path

**If $ARGUMENTS empty:** Ask user for path (e.g., `lit_review/papers/` or `lit_review/papers/00-background/`).

**If $ARGUMENTS provided:** Use path; resolve relative paths from project root.

---

### Step 2: Validate Directory

1. Verify the directory exists
2. Count PDF files recursively in the directory
3. If zero PDFs found, inform user and stop

---

### Step 3: Preview Changes

1. Find all PDF files recursively
2. For each file, compute the new filename after applying transformations:
   - Spaces → underscores (`_`)
   - Em dash (`—`) → hyphen (`-`)
   - En dash (`–`) → hyphen (`-`)
   - Smart quotes (`' ' " "`) → regular quotes (`' "`)
   - Accented characters → ASCII equivalents
3. Show a preview table of files that will be renamed (skip files that won't change)

Example preview:
```
Files to be renamed:
  1. Biswas - 2023 - Role of Chat GPT.pdf
     → Biswas_-_2023_-_Role_of_Chat_GPT.pdf

  2. Mello — 2024 — Denial.pdf
     → Mello_-_2024_-_Denial.pdf

Total: 2 files will be renamed
```

---

### Step 4: Execute Cleanup

Run the cleanup script:

```bash
.claude/skills/cleanup-pdf-names/scripts/cleanup_pdf_names.sh "{directory_path}"
```

---

### Step 5: Report Results

Report the summary from the script output:
- Number of files renamed
- Number of files skipped (target already exists)
- Any errors encountered

---

## Transformations Reference

| Character | Replacement |
|-----------|-------------|
| Space (` `) | Underscore (`_`) |
| Em dash (`—`) | Hyphen (`-`) |
| En dash (`–`) | Hyphen (`-`) |
| Left single quote (`'`) | Single quote (`'`) |
| Right single quote (`'`) | Single quote (`'`) |
| Left double quote (`"`) | Double quote (`"`) |
| Right double quote (`"`) | Double quote (`"`) |
| Accented chars (á, é, ñ, ü, etc.) | ASCII equivalents (a, e, n, u) |

---

## Edge Cases

### Target File Already Exists
Skip the file and report it. Do not overwrite existing files.

### Empty Directory
Report "No PDF files found in directory" and stop.

### Permission Errors
Report the specific file that failed and continue with remaining files.
