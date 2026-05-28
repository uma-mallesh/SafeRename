from core.cycle_resolution.cycle_analyzer import (
    CycleAnalyzer
)

from core.cycle_resolution.graph_rewriter import (
    GraphRewriter
)


class DeadlockResolver:

    def __init__(self):

        self.analyzer = (
            CycleAnalyzer()
        )

        self.rewriter = (
            GraphRewriter()
        )

    def resolve(

        self,

        schedule
    ):

        has_cycle = (

            self.analyzer.analyze(
                schedule
            )
        )

        if not has_cycle:

            return None

        rewritten = (

            self.rewriter.rewrite(
                schedule["execution_order"]
            )
        )

        return rewritten