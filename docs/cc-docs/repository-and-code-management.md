# Repository & Code Management

These skills keep your repository tidy and reproducible. Use them when starting new analysis scripts, updating directory documentation after adding or removing files, or auditing the state of your Python environment.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/create-script <path>` | Creates a new Python script at the specified path pre-populated with the project-standard header (purpose, notes, input, output, author) and a `main()` stub, so every script starts with consistent documentation and structure. |
| `/readme-clean <path>` | Audits and rewrites the `README.md` in the specified directory to match the project's canonical format, listing all current files and subdirectories with one-sentence descriptions; run this whenever you add or remove files from a directory. |
| `/generate-venv-report` | Generates a markdown report of the current virtual environment listing all installed packages and their versions; useful for documenting dependencies at a project milestone or debugging environment issues. |
