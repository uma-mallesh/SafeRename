from pathlib import Path

from core.virtual_filesystem.virtual_file import (
    VirtualFile
)

from core.virtual_filesystem.virtual_filesystem import (
    VirtualFilesystem
)

from core.virtual_filesystem.execution_plan import (
    ExecutionPlan
)

from core.virtual_filesystem.conflict_predictor import (
    detect_virtual_conflicts
)


class SimulationEngine:

    def run(self, scan_results):

        vfs = VirtualFilesystem()

        plan = ExecutionPlan()

        for item in scan_results:

            original_path = item["path"]

            cleaned_name = item["cleaned"]

            virtual_file = VirtualFile(

                original_name=Path(
                    original_path
                ).name,

                simulated_name=cleaned_name,

                path=original_path
            )

            vfs.add_file(
                virtual_file
            )

            plan.add_operation(

                original=Path(
                    original_path
                ).name,

                simulated=cleaned_name
            )

        conflicts = detect_virtual_conflicts(
            vfs
        )

        return {

            "vfs": vfs,

            "plan": plan,

            "conflicts": conflicts
        }