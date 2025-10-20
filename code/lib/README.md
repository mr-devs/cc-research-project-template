# Lib

This directory contains shared utility functions and helper libraries used across multiple scripts.
Library code promotes code reuse and maintains consistency across the project.

## Contents

- `pyproject.toml`: Modern Python packaging configuration (PEP 517/518 compliant)
- `setup.py`: Legacy setup script (retained for backwards compatibility)
- `lib/`: Package directory containing reusable modules for the project

## Installation

To install the package in development mode (editable install), navigate to this directory and run:

```bash
pip install -e .
```

This will work with both the modern `pyproject.toml` and legacy `setup.py` configurations.
