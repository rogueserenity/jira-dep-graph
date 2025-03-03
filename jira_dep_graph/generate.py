import argparse
import json
import os

from getpass import getpass
from jira import JIRA
from .graph import Graph
from .mermaid import create_graph


def get_credentials() -> dict:
    config_path = os.path.expanduser("~/.jira-dep-graph")
    if os.path.isfile(config_path):
        with open(config_path, "r") as config:
            json_credentials = json.load(config)
            return json_credentials
    else:
        endpoint = input("Jira Endpoint: ")
        user = input("Jira Email: ")
        api_token = getpass("Jira API Token: ")
        credentials = {
            "endpoint": endpoint,
            "user": user,
            "api_token": api_token,
        }
        json_credentials = json.dumps(credentials)
        with open(config_path, "w") as config:
            config.write(json_credentials)
        return credentials


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
    credentials = get_credentials()
    jira = JIRA(
        server=credentials["endpoint"],
        basic_auth=(credentials["user"], credentials["api_token"]),
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
