---
description: Clean README.md files in the entire repository or specified directories. $ARGUMENTS
argument-hint: [Include path(s) to clean]
---

# Task

You are a concise documentation expert.
Your goal is to clean up the README.md files included in the "Directories" section below.
If nothing is included in the "Directories" section below, then you should use the root directory of this project as the default directory of focus.

## Guidance

1. Before you begin, read the **Reference README** and use it as the canonical example for structure and tone within the README.md files that you edit or create:
   - **Reference README**: @/.claude/reference/reference-readme.md
2. Within the specified directories, search recursively for all subdirectories and content
3. For all subdirectories, either edit the existing README file to match the Reference README or create one to match it.
4. Edits should be made for the following reasons:
   (a) Items (scripts, other directories, data files, etc.) in a directory are not captured within the README and need to be included.
   (b) The descriptions in the README are no longer accurate. Check the items if you are unsure.
5. If there are no contents in the directory, generate the directory description to the best of your ability and an empty "Contents" section.
6. If you are unsure about something, ask the user questions to clarify.

## Directories

$ARGUMENTS
