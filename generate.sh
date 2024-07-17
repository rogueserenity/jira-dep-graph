#!/bin/sh

usage() {
    echo "Usage $0"
    printf "\t-d\t\tinclude completed issues\n"
    printf "\t-e\t\tthe epic (required)\n"
    printf "\t-f\t\timage format [svg|png|pdf] default: png\n"
    printf "\t-h\t\tthis usage message\n"
    exit 1
}

verify_poetry() {
    if ! command -v poetry > /dev/null 2>&1; then
        echo "poetry is required to be in your path"
        exit 1
    fi
}

verify_mermaid_cli() {
    if ! command -v mmdc > /dev/null 2>&1; then
        echo "mmdc (mermaid cli) is required to be in your path"
        exit 1
    fi
}

verify_poetry
verify_mermaid_cli

while getopts "de:f:h" FLAG; do
    case "${FLAG}" in
    d) DONE="YES"
    ;;
    e) EPIC="${OPTARG}"
    ;;
    f) FORMAT="${OPTARG}"
    ;;
    h) usage
    ;;
    *) usage
    ;;
    esac
done

if [ "${FORMAT}" = "" ]; then
    FORMAT="png"
fi

poetry run generate -e "${EPIC}" -o "${EPIC}.mmd" ${DONE:+"-d"} &&\
  mmdc -w 1920 -H 1080 -i "${EPIC}.mmd" -o "${EPIC}.${FORMAT}"
