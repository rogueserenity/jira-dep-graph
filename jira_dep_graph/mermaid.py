from .graph import Graph

graph_type = "flowchart LR"

status_class_def = """
    classDef TODO fill:#FE4040,color:#FFF
    classDef INPR fill:#FF8738
    classDef CREV fill:#F2F44B
    classDef TEST fill:#008800,color:#FFF
    classDef DONE fill:#3A62FE,color:#FFF
"""


dep_header = """
    subgraph Dependencies
        direction TB
"""

dep_footer = """
    end
"""


def create_key(include_done: bool) -> str:
    key = """
    subgraph Key
        direction TB
        AA[To Do]
        BB[In Progress]
        CC[Code Review]
        DD[Test]
"""

    if include_done:
        key += "        EE[Done]\n"
    else:
        key += "        EE[Done are removed]\n"

    key += """
        class AA TODO
        class BB INPR
        class CC CREV
        class DD TEST
        class EE DONE
    end
"""
    return key


def create_status_line(key: str, status: str) -> str:
    status_class = {
        "BACKLOG": "TODO",
        "TO DO": "TODO",
        "DISCOVERY": "INPR",
        "DESIGNING": "INPR",
        "ANALYSIS": "INPR",
        "IN DEVELOPMENT": "INPR",
        "IN PROGRESS": "INPR",
        "ACCEPTANCE": "CREV",
        "IN CODE REVIEW": "CREV",
        "CODE REVIEW": "CREV",
        "VALIDATION": "CREV",
        "UX REVIEW": "CREV",
        "IN LOCAL TEST": "TEST",
        "READY FOR LOCAL TESTING": "TEST",
        "READY FOR TEST": "TEST",
        "LOCAL TEST": "TEST",
        "READY FOR MERGE": "TEST",
        "READY FOR STAGING TEST": "TEST",
        "READY FOR STAGING": "TEST",
        "STAGING TEST": "TEST",
        "IN STAGING TEST": "TEST",
        "DEPLOY TO PRODUCTION": "TEST",
        "READY FOR PRODUCTION": "TEST",
        "READY FOR DEVELOPMENT": "DONE",
        "DONE": "DONE",
    }.get(status.upper())

    if status_class is None:
        print(f"Status: {status} is not mapped!")
    return f"        class {key} {status_class}\n"


def create_graph(graph: Graph) -> str:
    result = graph_type + "\n"
    result += status_class_def
    result += create_key(graph.include_done)
    result += dep_header

    for node in graph.nodes.items():
        result += f"        {node[0]}\n"

    result += "\n\n"

    for dep in graph.dependencies:
        result += f"        {dep[0]} --> {dep[1]}\n"

    if graph.dependencies:
        result += "\n\n"

    for node in graph.nodes.items():
        result += create_status_line(node[0], node[1])

    result += dep_footer

    return result
