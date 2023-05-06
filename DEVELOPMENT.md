# Development Guidelines

## Requirements

- Python >= 3.9
- Poetry

## Getting started

```sh
## How to use poetry

# 1 - Install dependencies
$ poetry install
# 2 - Load dependencies
$ poetry shell
# to run tests
$ pytest .
# to run tox
$ tox

# code formatter and linter will run at git commit
# however, you can run yourself

# to run code formatter
$ black .
# to run code linter
$ flake8 .

# to exit poetry shell (ctrl+d) or exit
```
