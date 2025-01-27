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


## Wrapper Script

Included in the root of this repository is a wrapper script that will execute the python script and then run the mermaid generation from the created `mmd` file. To execute the script:

```
$ ./generate.sh -h
Usage ./generate.sh
        -d              include completed issues
        -e              the epic (required)
        -f              image format [svg|png|pdf] default: png
        -h              this usage message
```

This requires that the [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) be installed and `mmdc` be in your path. You will most likely want `nvm` in your path as well,
and try running:

        nvm use

before running the wrapper script to ensure you have the proper version of `node.js` installed.
