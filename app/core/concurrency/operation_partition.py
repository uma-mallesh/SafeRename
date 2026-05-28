class OperationPartitioner:

    def partition(self, operations):

        partitions = []

        current = []

        seen_targets = set()

        for operation in operations:

            source = operation["source"]

            target = operation["target"]

            if (
                source in seen_targets
                or
                target in seen_targets
            ):

                partitions.append(current)

                current = []

                seen_targets.clear()

            current.append(operation)

            seen_targets.add(source)

            seen_targets.add(target)

        if current:

            partitions.append(current)

        return partitions