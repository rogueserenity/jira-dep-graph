import argparse
import json
import os

from getpass import getpass
from jira import JIRA
from .graph import Graph
from .mermaid import create_graph


def get_creds() -> tuple[str, str]:
    config_path = os.path.expanduser("~/.jira-creds")
    if os.path.isfile(config_path):
        with open(config_path, "r") as config:
            json_creds = json.load(config)
            return (json_creds[0], json_creds[1])
    else:
        user = input("Jira Email: ")
        api_token = getpass("Jira API Token: ")
        creds = (user, api_token)
        json_creds = json.dumps(creds)
        with open(config_path, "w") as config:
            config.write(json_creds)
        return creds


def parse_args() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--epic", help='epic key e.g. "TR-2413"')
    parser.add_argument(
        "-d",
        "--done",
        help="display done issues",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file, defaults to stdout",
        type=argparse.FileType("w", encoding="utf-8"),
    )

    args = parser.parse_args()

    result = {}
    result["epic"] = args.epic
    result["done"] = args.done
    result["output"] = args.output

    if result["epic"] is None:
        result["epic"] = input("Epic Key: ")

    return result


def generate():
    jira = JIRA(
        server="https://jumpcloud.atlassian.net",
        basic_auth=get_creds(),
    )

    args = parse_args()
    graph = Graph(jira, args["epic"])
    if not args["done"]:
        graph.remove_done()

    mermaid = create_graph(graph)
    if args["output"] is not None:
        out = args["output"]
        out.write(mermaid)
    else:
        print(mermaid)
