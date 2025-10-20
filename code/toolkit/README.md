# Toolkit

This directory contains the local project module with shared utility functions and project-specific code used across multiple scripts.
This promotes code reuse and maintains consistency across the project.

## Contents

- `pyproject.toml`: Modern Python packaging configuration (PEP 517/518 compliant)
- `setup.py`: Legacy setup script (retained for backwards compatibility)
- `toolkit/`: Package directory containing reusable modules for the project

## Installation

To install the package in development mode (editable install), navigate to this directory and run:

```bash
pip install -e .
```

This will work with both the modern `pyproject.toml` and legacy `setup.py` configurations.
