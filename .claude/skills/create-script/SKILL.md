---
name: create-script
description: Create a new Python script following project best practices. $ARGUMENTS
argument-hint: [Description of what the script should do.]
disable-model-invocation: true
---

# Task

You are a computational social science research assistant specializing in creating rigorous, reproducible scientific code.
Your goal is to create a new Python script that follows the project's coding standards and best practices.

## Script Description

> $ARGUMENTS

## Guidance

1. Before you begin, do these two things:

   - Read the **Reference Script** and **Project Standards** to understand the canonical template and structure:

     - **Reference Script**: @.claude/skills/create-script/reference-script.py
     - **Project Standards**: @CLAUDE.md

   - If the script type is already known from the description, **also read the corresponding type-specific reference file**:
     - Data collection (`code/data_collection/`) → @.claude/skills/create-script/reference-data-collection.py
     - Data cleaning (`code/cleaning/`) → @.claude/skills/create-script/reference-data-cleaning.py
     - Figure generation (`code/generate_figures/`) → @.claude/skills/create-script/reference-figure-generation.py
     - Table generation (`code/generate_tables/`) → @.claude/skills/create-script/reference-table-generation.py

     If the type is unclear, read the appropriate file after Step 2 confirms the script location.

   - Reference anything else mentioned by the user in the "Script Description" section so that you have full context before moving forward

2. Ask the user to clarify the following (if not already clear from the description):

   - **Script Location**: Where should this script be saved? Suggest an appropriate location based on the script's purpose:

     - `code/data_collection/` for data gathering scripts
     - `code/cleaning/` for data preprocessing scripts
     - `code/analysis/` for primary analysis pipelines
     - `code/generate_figures/` for plot & visualization scripts
     - `code/generate_tables/` for table generation scripts (LaTeX/CSV outputs)
     - `code/generate_reports/` for simple `.txt` statistics reports
     - `code/misc/` for scripts that don't fit elsewhere

   - **Input Sources**: What are the inputs to this script?

     - Files (provide paths)
     - Command-line arguments
     - External data sources
     - Other dependencies

   - **Output Location**: Where should outputs be saved? Suggest appropriate locations:

     - `data/processed/` for cleaned, documented data
     - `data/interim/` for intermediate processing files
     - `results/figures/` for publication-ready plots
     - `results/tables/` for formatted results
     - `data/logs/` for log files

   - **Implementation Details**: Clarify any ambiguities about:
     - Data processing steps or transformations
     - Analysis methods or algorithms to use
     - Expected output format and structure
     - Any assumptions that should be documented

3. **Check for code reuse (DRY Principle - Don't Repeat Yourself)**:

   - Search the directory where the new script will be saved for existing scripts
   - Look for similar functionality or shared logic across scripts
   - If you find repeated code patterns or utility functions:
     - Flag the reusable pattern(s) to the user and propose extracting them to `toolkit/`
     - Do **not** modify existing scripts without explicit user approval — only the new script is in scope unless the user agrees to broaden the work

4. Once you have clarity, create the script prioritizing **clarity over speed**.

   - Remember to base the file on @.claude/skills/create-script/reference-script.py template and structure

5. **Update the directory README**:

   - After creating the script, edit the README.md file in the same directory
   - Add an entry for the new script in the "Contents" section
   - Include a one-sentence description of what the script does
   - Ensure the README accurately reflects all directory contents

6. After creating the script:
   - Explain what you created and where it was saved
   - Note any code that was refactored into `toolkit/` (if applicable)
   - Note any assumptions you made and potential "gotchas"
   - Suggest next steps (e.g., testing, data collection)

## Best Practices Checklist

- [ ] Script header docstring is complete (Purpose, Notes, Input, Output, Author)
- [ ] Imports organized (standard → third-party → local)
- [ ] Constants defined in UPPERCASE
- [ ] All functions have NumPy/Pandas style docstrings
- [ ] `os.chdir(Path(__file__).resolve().parent)` included
- [ ] Relative paths used throughout
- [ ] `main()` function orchestrates workflow
- [ ] Code prioritizes readability and reproducibility
- [ ] Assumptions and decisions are documented in comments
- [ ] Checked for duplicate code; refactored shared logic to `toolkit/` if needed
- [ ] Directory README.md updated to include the new script
- [ ] Type-specific patterns applied (e.g., logging/resume for collection, argparse for cleaning, rcParams/dual output for figures, totals row/to_latex for tables)
