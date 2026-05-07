# Data Exploration: Mobility in Humans and Animals

This repository accompanies the course "Mobility in Humans and Animals: A data exploration".
It offers an overview on movement and mobility in animals and humans from a data-driven perspective. It will cover micro- to macroscopic movement from animals and humans, collective decision making during movement processes and transport networks.
Within this repo the students will analyze the datasets in jupyter-notebooks.

## Install

Using conda:

1. `conda env create -f env.yml`
2. `conda activate mobha`

Using an existing environment:

1. `python -m pip install -e .`

Using uv as package manager (and dev mode):

## Update the environment

During the course, we will add packages that you need for different analysis. They will be added to your `env.yml` file.

In order to update your environment run:

```bash
mamba env update --file env.yml --prune
```

if `mamba` is not available use `conda` instead.

1. `uv sync --dev`

## Repository layout

* `src/mobha/`: package source code to analyze animal mobility
* `tests/`: pytest-based tests
* `env.yml`: optional conda environment with notebook and analysis tooling
* `pyproject.toml`: package metadata, build backend, and tool configuration
* `README.md`: project overview and setup notes

## Recommended defaults

* keep the core analysis stack aligned between `env.yml` and `[project.dependencies]`
* keep development-only tools in `[dependency-groups].dev` when using uv
* use the package environment for notebooks so students get consistent analysis tooling
