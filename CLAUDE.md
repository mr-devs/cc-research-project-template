# Computational Social Science Research Best Practices

We're building rigorous, reproducible research together.
Listed below are the best practices we agree to follow.

## 1. Goals

Above all else, we are striving for high-quality, reproducible scientific code.
It should prioritize **clarity over speed**, so that others can understand it and reproduce it.
This means that we will document assumptions and rationale for data collection, wrangling, and analysis decisions with comments throughout the code.

## 2. Coding & Documentation Standards

### 2.1a  Python Script Header

```python
"""
Purpose:
    Brief description of the scripts purpose.

Notes:
    Include details about how the script works, assumptions/decisions made so that independent reviewers can understand how analyses were done.

Input:
    - List of input files, command-line flags, etc. are saved here.

Output:
    - Generated files with the full output format.
    - Should include pertinent information about the data. For example, columnar data should include a list of the columns and their definitions.

Author: Matthew DeVerna
"""
```

### 2.1b  Python Module Header

Include only a brief description of the module purpose.
For example, a module file called `utils.py` might look like this.

```python
"""
Convenience utility functions are saved here.
"""

# Imports ...
# Functions ...
```

### 2.2  Script Organization

- Imports → constants (UPPERCASE, grouped) → functions/classes → `main()`
- Use `pathlib` and `os` for paths.
- Add `os.chdir(Path(__file__).resolve().parent)` at top of **ALL SCRIPTS** and use relative paths so that scripts run when called from any location.
- Scripts should be organized for **simplicity** and **readability** for a wide scientific audience.

### 2.3  Function Docstrings (Pandas / NumPy style)

```python
def calculate_demographic_shift(df, baseline_year, target_year):
    """
    Return the percentage change in demographic groups between two years.

    Parameters
    ----------
    df : pandas.DataFrame
        Census data with demographic information and time series.
    baseline_year : int
        The starting year for the comparison.
    target_year : int
        The ending year for the comparison.

    Returns
    -------
    pandas.DataFrame
        A DataFrame showing the percent change in demographic group sizes
        between `baseline_year` and `target_year`.
    """
```

### 2.4  Directory‑Level README

Every directory _must_ contain a `README.md` file that lists the purpose of the directory and contents.
It should be updated whenever the contents change.

See @.claude/reference/reference-readme.md and use it as the canonical example for structure and tone.

## 3  Project Structure (Template)

```
code/
  analysis/          # Primary analysis pipelines
  cleaning/          # Data preprocessing scripts
  data_collection/   # Data gathering scripts
  generate_figures/  # Plot & visualization scripts
  generate_tables/   # Table generation scripts (e.g. latex)
  generate_reports/  # Scripts generating simply .txt statistics reports
  toolkit/           # Local module with project-specific code
  misc/              # Anything that doesn't fit clearly in other directories
  notebooks/         # Exploratory notebooks
  tests/             # Unit tests & validation

data/
  external/          # Third‑party reference data
  interim/           # Intermediate data processing files
  logs/              # Output log files
  misc/              # Anything that doesn't fit clearly in other directories
  processed/         # Cleaned, documented data
  raw/               # Immutable originals

results/
  figures/           # Publication‑ready plots
  tables/            # Formatted results
  reports/           # Simple .txt reports of statistics

workflow/
  Snakefile          # Optional orchestration file that coordinates the below pipelines
  analyze/           # Analysis pipeline
    Snakefile        # Snakemake workflow for analysis
  clean/             # Data cleaning pipeline
    Snakefile        # Snakemake workflow for cleaning data
  collect/           # Data collection pipeline
    Snakefile        # Snakemake workflow for collecting data
  visualize/         # Figure generation pipeline
    Snakefile        # Snakemake workflow for creating final visualizations
```

## 4  Virtual Environment Management

Use [uv](https://docs.astral.sh/uv/) to manage Python virtual environments.

```bash
# Create a new virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Install packages
uv pip install <package>

# Install from requirements file
uv pip install -r requirements.txt
```
