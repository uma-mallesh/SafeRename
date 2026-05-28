from pathlib import Path

from core.concurrency.worker_pool import (
    WorkerPool
)

from core.concurrency.operation_partition import (
    OperationPartitioner
)

from core.concurrency.execution_metrics import (
    ExecutionMetrics
)


class ConcurrentExecutor:

    def __init__(self):

        self.pool = WorkerPool()

        self.partitioner = (
            OperationPartitioner()
        )

        self.metrics = (
            ExecutionMetrics()
        )

    def execute_operation(

        self,

        operation
    ):

        source = operation["source"]

        target = operation["target"]

        Path(source).rename(target)

        return {

            "source": source,

            "target": target,

            "status": "success"
        }

    def execute(

        self,

        operations
    ):

        self.metrics.start()

        partitions = (

            self.partitioner.partition(
                operations
            )
        )

        results = []

        for partition in partitions:

            futures = []

            for operation in partition:

                future = (

                    self.pool.submit(

                        self.execute_operation,

                        operation
                    )
                )

                futures.append(future)

            for future in futures:

                results.append(
                    future.result()
                )

        self.metrics.stop()

        return {

            "results": results,

            "duration": (

                self.metrics.duration()
            )
        }