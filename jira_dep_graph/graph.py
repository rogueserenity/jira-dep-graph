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

        status = str(issue.get_field("status"))
        self.nodes.update({issue.key: status})

        subtasks = issue.get_field("subtasks")
        if len(subtasks) > 0:
            for st in subtasks:
                dependency = (issue.key, st.key)
                self.dependencies.append(dependency)
                self.__build(st)

        links = issue.get_field("issuelinks")
        for link in links:
            if str(link.type) == "Blocks":
                if hasattr(link, "inwardIssue"):
                    dependency = (issue.key, link.inwardIssue.key)
                    self.dependencies.append(dependency)
                    self.__build(link.inwardIssue)

    def remove_done(self):
        self.include_done = False
        nodes = {
            key: val for key, val in self.nodes.items() if val not in done_statuses
        }
        deps = [x for x in self.dependencies if x[0] in nodes and x[1] in nodes]

        self.nodes = nodes
        self.dependencies = deps
