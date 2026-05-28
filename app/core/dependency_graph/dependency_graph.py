class DependencyGraph:

    def __init__(self):

        self.nodes = []

    def add_node(self, node):

        self.nodes.append(node)

    def all_nodes(self):

        return self.nodes