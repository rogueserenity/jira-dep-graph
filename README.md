# JIRA Dependency Graph

## What it does

This will generate a [Mermaid](https://mermaid.js.org/) dependency graph for a specified JIRA Epic.

## Dependencies

User must first install [poetry](https://python-poetry.org/)

## Installation

1. Clone this repo
2. Run

        poetry install


## Usage

```
poetry run generate --help
usage: generate [-h] [-e EPIC]

options:
  -h, --help            show this help message and exit
  -e EPIC, --epic EPIC  epic key e.g. "TR-2413"
```
If you do not pass an epic at the command line, the utility will prompt you for it.

The first time the script is run, it will require a JIRA username and API Token. These are stored in `~/.jira-creds`. To rotate the token, simply delete the file and re-run the script.
