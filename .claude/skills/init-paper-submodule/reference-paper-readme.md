# Git submodules

This directory is meant to live as a [**git submodule**](https://git-scm.com/book/en/v2/Git-Tools-Submodules) of [this repository](<PARENT_REPO_URL>).
Please visit this other repository README.md file for instructions about including.

Assuming you have done the above, this file should be living in a directory called "`paper/`".
Using a submodule means `paper/` is its own independent git repository nested inside the larger project's "parent" repository.
The parent repository only records a pointer (a specific commit) to the submodule, not the submodule's actual files.

## Why?

We do this so that we can link only this directory to our Overleaf project without needing to include all of the code and data from the larger project within the Overleaf project.

## How to use submodules in this project

Crash course (but probably you should just ask your coding agent).

### Cloning

When cloning this repository, the `paper/` directory will be empty by default. To populate it, either clone with `--recurse-submodules`:

```bash
git clone --recurse-submodules <PARENT_REPO_SSH_URL>
```

…or, if you have already cloned without that flag, initialize the submodule afterwards:

```bash
git submodule update --init --recursive
```

### Pulling updates

To pull the latest changes from the paper submodule along with the parent repo:

```bash
git pull --recurse-submodules
```

Or update just the submodule to the latest commit on its tracked branch:

```bash
git submodule update --remote paper
```

### Changes inside `paper/` must be pushed separately

This is the most common source of confusion. **Commits made inside `paper/` are not pushed when you push the parent repository.** The two repos have independent histories.

When you edit files inside `paper/`, the workflow is:

1. **Commit and push inside the submodule first:**

   ```bash
   cd paper
   git add <files>
   git commit -m "..."
   git push
   ```

2. **Then commit the updated submodule pointer in the parent repo:**

   ```bash
   cd ..
   git add paper
   git commit -m "Bump paper submodule"
   git push
   ```

If you skip step 1, anyone else pulling the parent repo will get a submodule pointer to a commit that doesn't exist on the remote, and `git submodule update` will fail for them.
