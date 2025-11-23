# Virtual Environment Report

High-level next steps that the reader of this report should take:

- [example] Confirm the Python version and document it in the project root `README.md`.
- [example] Maintain a minimal `requirements.txt` with only core pipeline dependencies.
- [example] Add instructions in the project root `README.md` for installing any local project packages.
- [example] Add brief notes in the project root `README.md` about other required software (e.g., Snakemake, R, system tools).

(Replace the examples above with project-specific bullets.)

---

## Python version

This project is currently using Python version: `X.XX`.

### Next steps

1. Document this Python version in the project root `README.md`.
2. Optionally add a short note about how to install or manage this Python version (e.g., `pyenv`, Conda, system package manager).

---

## Python `requirements.txt` file

This project leverages **N** third-party Python packages that need to be installed to run the **core replication pipeline**:

- Third-party pipeline packages:
  1. `package_1==1.97.1`
  2. `package_2==23.0.1`

(Replace `N`, `package_1`, etc. with project-specific values.)

### Next steps

1. Ensure a minimal `requirements.txt` exists in the project root directory containing only these core pipeline packages.
2. In the project root `README.md`, add instructions for:
   - Creating a virtual environment.
   - Installing dependencies via `pip install -r requirements.txt`.

---

## Local project repository packages

This project leverages **M** local packages used in the core pipeline:

- Local packages:
  1. `local_package_1`
  2. `local_package_2`

### Next steps

1. In the project root `README.md`, add clear instructions for installing any local packages (e.g., `pip install -e .` or `pip install -e src/`).
2. Place these instructions after the virtual environment and `requirements.txt` setup steps.

---

## Other required software

Other software used to replicate the code in this repository (beyond Python packages) should be listed here:

- `software_1` (e.g., Snakemake CLI, R, `ffmpeg`, `graphviz`, LaTeX)
- `software_2`

### Next steps

1. In the project root `README.md`, briefly describe each required tool and how it is used in the pipeline.
2. If installation is non-trivial, include links or short guidance for installing these tools.
