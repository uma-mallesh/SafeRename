class CycleDetector:

    def detect(self, graph):

        visited = set()

        stack = set()

        def visit(node):

            if node in stack:
                return True

            if node in visited:
                return False

            visited.add(node)

            stack.add(node)

            for dependency in node.dependencies:

                if visit(dependency):

                    return True

            stack.remove(node)

            return False

        for node in graph.all_nodes():

            if visit(node):

                return True

        return False