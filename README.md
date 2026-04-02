# minimal-template

Minimal Python template repository for keeping project-specific code in `src/minimal_template`.

## What changed

This template now uses a modern Python packaging layout:

* package code lives under `src/`
* `pyproject.toml` is the single source of packaging configuration
* editable installs work without `setup.py`
* tests validate the installed package metadata instead of using a dummy failing test

## Install

Using conda:

1. `conda env create -f env.yml`
2. `conda activate mini_template`

Using an existing environment:

1. `python -m pip install -e .`

Using uv as package manager (and dev mode):

1. `uv sync --dev`

## Repository layout

* `src/minimal_template/`: package source code
* `tests/`: pytest-based tests
* `env.yml`: optional conda environment with notebook and analysis tooling
* `pyproject.toml`: package metadata, build backend, and tool configuration
* `README.md`: project overview and setup notes

## Recommended defaults

* keep runtime dependencies in `[project.dependencies]`
* keep development-only tools in `[dependency-groups].dev` when using uv
* keep notebooks and analysis tooling out of the package metadata unless they are runtime requirements
* prefer `python -m pip install -e .` for local development

## Notebook Git filter

If you keep notebooks in [./notebooks](./notebooks), the included [./notebooks/.gitattributes](./notebooks/.gitattributes) can be used together with a local Git filter that strips notebook output on commit:

```gitattributes
*.ipynb filter=strip-notebook-output
```

```ini
[filter "strip-notebook-output"]
    clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
```
