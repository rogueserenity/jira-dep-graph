done_statuses = ["Done", "Ready for Development"]


class Graph:
    def __init__(self, jira, epic):
        issue = jira.issue(epic)
        issue_type = str(issue.get_field("issuetype"))
        assert issue_type == "Epic", f"{epic} is not an Epic!"

        self.jira = jira
        self.epic = issue
        self.include_done = True
        self.nodes = {}
        self.dependencies = []

        children = jira.search_issues(f"linkedIssue = {epic}")
        for child in children:
            if child.key == epic:
                continue
            self.__build(child)

    def __build(self, issue):
        if issue.key in self.nodes:
            return

        if not hasattr(issue, "issuelinks"):
            issue = self.jira.issue(issue.key)

        self.nodes.update({issue.key: str(issue.get_field("status"))})

        links = issue.get_field("issuelinks")
        for link in links:
            if str(link.type) == "Blocks":
                if hasattr(link, "inwardIssue"):
                    dependency = (issue.key, link.inwardIssue.key)
                    self.dependencies.append(dependency)
                    self.__build(link.inwardIssue)

    def remove_done(self):
        self.include_done = False
        done = []
        for node in self.nodes.items():
            if node[1] in done_statuses:
                done.append(node[0])

        for d in done:
            del self.nodes[d]
            for dep in self.dependencies:
                if dep[0] == d or dep[1] == d:
                    self.dependencies.remove(dep)
