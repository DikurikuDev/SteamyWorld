# SteamyWorld

A game modding CLI tool to handle Steamworld games assets.

## Features

- compression/decompression

## Games supported

- SteamWorld Dig 2
- SteamWorld Heist
- SteamWorld Quest Hand of Gilgamech

## Requirement

- Python3+
- Poetry

## Getting started (Using)

```sh
#  to run the code:
#  1 - Install dependencies.
$ poetry install
#  2 - Load dependencies.
$ poetry shell
#  Now you can use Python and the dependencies installed.
$ python ./src/cli.py

# To decompress without print log:
$ steamy --quiet ~/GOG Games/SteamWorld Heist/

# To compress or decompress:
$ steamy --compress ~/GOG Games/SteamWorld Heist/
$ steamy --decompress ~/GOG Games/SteamWorld Heist/
```

## Getting started (Developing)

```sh
#  to run the code:
#  1 - Install dependencies.
$ poetry install
#  2 - Load dependencies.
$ poetry shell
#  Now you can use Python and the dependencies installed.
$ python ./src/cli.py
#  To run tests:
$ pytest ./
#  To exit poetry shell (ctrl+d) or:
$ exit

# -----

#  Before starting a new project:
#  Make sure that when you commit, the code formatter and linter will run
# automatically. If not:
$ pre-commit install

# -----

#  Before push to main, is nice to text if tox is working
$ tox

# -----

#  The code formatter and linter will run at git commit. However, you can run
# yourself:

#  To run code formatter:
$ black ./
#  To run code linter
$ flake8 ./
```

