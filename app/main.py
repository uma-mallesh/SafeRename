import customtkinter as ctk

from tkinter import filedialog
from pathlib import Path

# =========================================================
# SCANNER
# =========================================================

from core.scanner.file_scanner import scan_folder

# =========================================================
# TRANSACTION ENGINE
# =========================================================

from core.transaction_engine.transaction_manager import (
    TransactionManager
)

# =========================================================
# VIRTUAL FILESYSTEM / SIMULATION
# =========================================================

from core.virtual_filesystem.simulation_engine import (
    SimulationEngine
)

# =========================================================
# COLLISION HANDLER
# =========================================================

from core.rename_engine.collision_handler import (
    resolve_collision
)

# =========================================================
# ROLLBACK
# =========================================================

from core.rename_engine.rollback_manager import (
    save_rollback,
    load_rollback,
    clear_rollback
)

# =========================================================
# UNDO ENGINE
# =========================================================

from core.rename_engine.undo_engine import (
    undo_renames
)

# =========================================================
# VALIDATION
# =========================================================

from core.rename_engine.transaction_validator import (
    validate_transaction
)

# =========================================================
# TRANSACTION QUEUE
# =========================================================

from core.rename_engine.transaction_queue import (
    TransactionQueue
)

# =========================================================
# WORKERS
# =========================================================

from core.workers.scan_worker import ScanWorker

from core.workers.rename_worker import RenameWorker

# =========================================================
# OPERATION STATE
# =========================================================

from core.state.operation_state import (
    OperationState
)

# =========================================================
# PERSISTENCE / RECOVERY
# =========================================================

from core.persistence.operation_journal import (
    write_journal
)

from core.persistence.recovery_manager import (
    detect_interrupted_operations
)

from core.persistence.state_snapshot import (
    save_snapshot
)

# =========================================================
# THEME
# =========================================================

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


# =========================================================
# MAIN APPLICATION
# =========================================================

class SafeRenameApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # =================================================
        # WINDOW CONFIGURATION
        # =================================================

        self.title("SafeRename")

        self.geometry("1250x920")

        self.minsize(1100, 760)

        # =================================================
        # CORE STATE
        # =================================================

        self.results = []

        self.transaction_queue = TransactionQueue()

        self.operation_state = OperationState()

        self.transaction_manager = (
            TransactionManager()
        )

        self.simulation_engine = (
            SimulationEngine()
        )

        # =================================================
        # HEADER
        # =================================================

        self.title_label = ctk.CTkLabel(
            self,
            text="SafeRename 🚀",
            font=("Arial", 38, "bold")
        )

        self.title_label.pack(
            pady=(20, 5)
        )

        self.subtitle_label = ctk.CTkLabel(
            self,
            text=(
                "Predictive Atomic Filesystem "
                "Orchestration Platform"
            ),
            font=("Arial", 16)
        )

        self.subtitle_label.pack(
            pady=(0, 20)
        )

        # =================================================
        # BUTTON FRAME
        # =================================================

        self.button_frame = ctk.CTkFrame(self)

        self.button_frame.pack(
            pady=10
        )

        # =================================================
        # SCAN BUTTON
        # =================================================

        self.scan_button = ctk.CTkButton(
            self.button_frame,
            text="Select Folder & Scan",
            command=self.select_folder,
            width=220,
            height=44
        )

        self.scan_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # =================================================
        # EXECUTE BUTTON
        # =================================================

        self.rename_button = ctk.CTkButton(
            self.button_frame,
            text="Execute Transaction",
            command=self.rename_files,
            fg_color="darkgreen",
            hover_color="green",
            width=220,
            height=44
        )

        self.rename_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # =================================================
        # UNDO BUTTON
        # =================================================

        self.undo_button = ctk.CTkButton(
            self.button_frame,
            text="Undo Transaction",
            command=self.undo_last_rename,
            fg_color="darkred",
            hover_color="red",
            width=220,
            height=44
        )

        self.undo_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # =================================================
        # CANCEL BUTTON
        # =================================================

        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel Operation",
            command=self.cancel_operation,
            fg_color="orange",
            hover_color="darkorange",
            width=220,
            height=44
        )

        self.cancel_button.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

        # =================================================
        # STATUS FRAME
        # =================================================

        self.status_frame = ctk.CTkFrame(self)

        self.status_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # =================================================
        # STATUS LABEL
        # =================================================

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Status: Idle",
            font=("Arial", 14)
        )

        self.status_label.pack(
            pady=10
        )

        # =================================================
        # PROGRESS BAR
        # =================================================

        self.progress_bar = ctk.CTkProgressBar(
            self.status_frame,
            width=900,
            height=18
        )

        self.progress_bar.pack(
            pady=10
        )

        self.progress_bar.set(0)

        # =================================================
        # METRICS LABEL
        # =================================================

        self.metrics_label = ctk.CTkLabel(
            self.status_frame,
            text="Processed: 0 / 0",
            font=("Arial", 13)
        )

        self.metrics_label.pack(
            pady=(0, 10)
        )

        # =================================================
        # RESULTS OUTPUT
        # =================================================

        self.results_box = ctk.CTkTextbox(
            self,
            width=1150,
            height=640,
            font=("Consolas", 13)
        )

        self.results_box.pack(
            pady=20,
            padx=20,
            fill="both",
            expand=True
        )

        # =================================================
        # RECOVERY CHECK
        # =================================================

        self.check_recovery_state()

    # =====================================================
    # RECOVERY DETECTION
    # =====================================================

    def check_recovery_state(self):

        interrupted = detect_interrupted_operations()

        if interrupted:

            self.results_box.insert(
                "end",
                (
                    "⚠ Interrupted operations detected.\n"
                    f"{len(interrupted)} "
                    f"incomplete tasks found.\n\n"
                )
            )

    # =====================================================
    # SELECT FOLDER
    # =====================================================

    def select_folder(self):

        folder_selected = filedialog.askdirectory()

        if not folder_selected:
            return

        self.results_box.delete(
            "1.0",
            "end"
        )

        self.progress_bar.set(0)

        self.metrics_label.configure(
            text="Processed: 0 / 0"
        )

        self.results_box.insert(
            "end",
            (
                "==================================================\n"
                "SCAN SESSION STARTED\n"
                "==================================================\n\n"
            )
        )

        self.results_box.insert(
            "end",
            (
                f"Scanning Folder:\n"
                f"{folder_selected}\n\n"
            )
        )

        self.status_label.configure(
            text="Status: Scanning..."
        )

        # =================================================
        # SAVE SNAPSHOT
        # =================================================

        save_snapshot({

            "last_selected_folder": folder_selected,

            "status": "scanning"
        })

        # =================================================
        # BACKGROUND SCAN
        # =================================================

        def scan_task():

            return scan_folder(
                folder_selected
            )

        worker = ScanWorker(
            scan_task,
            self.on_scan_complete
        )

        worker.start()

    # =====================================================
    # SCAN CALLBACK
    # =====================================================

    def on_scan_complete(self, results):

        self.results = results

        self.after(
            0,
            self.display_scan_results
        )

    # =====================================================
    # DISPLAY SCAN RESULTS
    # =====================================================

    def display_scan_results(self):

        self.status_label.configure(
            text="Status: Scan Complete"
        )

        if not self.results:

            self.results_box.insert(
                "end",
                "✅ No problematic filenames found.\n"
            )

            return

        self.results_box.insert(
            "end",
            (
                f"⚠ Found "
                f"{len(self.results)} "
                f"problematic files:\n\n"
            )
        )

        for item in self.results:

            preview_text = (

                f"ORIGINAL:\n"
                f"{item['original']}\n\n"

                f"CLEANED:\n"
                f"{item['cleaned']}\n"

                f"{'-' * 80}\n"
            )

            self.results_box.insert(
                "end",
                preview_text
            )

    # =====================================================
    # START TRANSACTION
    # =====================================================

    def rename_files(self):

        if not self.results:

            self.results_box.insert(
                "end",
                "\n❌ No scan results available.\n"
            )

            return

        self.status_label.configure(
            text="Status: Running Simulation..."
        )

        worker = RenameWorker(
            self.perform_transaction_operations,
            self.on_transaction_complete
        )

        worker.start()

    # =====================================================
    # TRANSACTION PIPELINE
    # =====================================================

    def perform_transaction_operations(self):

        self.operation_state.reset()

        self.operation_state.total_operations = len(
            self.results
        )

        self.transaction_queue.clear()

        rollback_log = []

        # =================================================
        # SIMULATION ENGINE
        # =================================================

        simulation = (
            self.simulation_engine.run(
                self.results
            )
        )

        conflicts = simulation["conflicts"]

        # =================================================
        # CONFLICT DETECTION
        # =================================================

        if conflicts:

            self.results_box.insert(

                "end",

                (
                    "\n⚠ Predicted conflicts detected:\n\n"
                )
            )

            for conflict in conflicts:

                self.results_box.insert(

                    "end",

                    f"{conflict}\n"
                )

            return {

                "success": False,

                "rollback_log": [],

                "transaction": None
            }

        # =================================================
        # EXECUTION PLAN
        # =================================================

        plan = simulation["plan"]

        self.results_box.insert(

            "end",

            (
                "\n==================================================\n"
                "SIMULATION PLAN\n"
                "==================================================\n\n"
            )
        )

        for operation in plan.operations:

            self.results_box.insert(

                "end",

                (
                    f"{operation['original']}\n"
                    f"→ {operation['simulated']}\n\n"
                )
            )

        # =================================================
        # CREATE TRANSACTION
        # =================================================

        transaction = (
            self.transaction_manager
            .create_transaction()
        )

        # =================================================
        # STAGE TRANSACTION OPERATIONS
        # =================================================

        for item in self.results:

            if self.operation_state.cancel_requested:

                break

            try:

                original_path = item["path"]

                original_file = Path(
                    original_path
                )

                directory = original_file.parent

                cleaned_name = item["cleaned"]

                # -----------------------------------------
                # COLLISION RESOLUTION
                # -----------------------------------------

                safe_name = resolve_collision(

                    directory,

                    cleaned_name
                )

                target_path = str(
                    Path(directory) / safe_name
                )

                # -----------------------------------------
                # VALIDATION
                # -----------------------------------------

                issues = validate_transaction(

                    original_path,

                    safe_name
                )

                if issues:

                    continue

                # -----------------------------------------
                # JOURNAL ENTRY
                # -----------------------------------------

                journal_entry = {

                    "original": original_path,

                    "target": target_path,

                    "completed": False
                }

                write_journal(
                    journal_entry
                )

                # -----------------------------------------
                # TRANSACTION QUEUE
                # -----------------------------------------

                self.transaction_queue.add({

                    "original": original_path,

                    "target": target_path
                })

                # -----------------------------------------
                # STAGE TRANSACTION
                # -----------------------------------------

                transaction.add_operation(

                    original_path,

                    target_path
                )

                rollback_log.append({

                    "old": original_path,

                    "new": target_path
                })

                # -----------------------------------------
                # UPDATE STATE
                # -----------------------------------------

                self.operation_state.increment_completed()

                progress = (
                    self.operation_state
                    .progress_percentage()
                )

                self.after(

                    0,

                    lambda p=progress:
                    self.update_progress(p)
                )

            except Exception as error:

                self.results_box.insert(

                    "end",

                    (
                        "❌ STAGING ERROR:\n"
                        f"{str(error)}\n\n"
                    )
                )

        # =================================================
        # COMMIT TRANSACTION
        # =================================================

        success = (

            self.transaction_manager.commit(
                transaction
            )
        )

        # =================================================
        # SAVE ROLLBACK
        # =================================================

        if success:

            save_rollback(
                rollback_log
            )

        return {

            "success": success,

            "rollback_log": rollback_log,

            "transaction": transaction
        }

    # =====================================================
    # UPDATE PROGRESS
    # =====================================================

    def update_progress(self, progress):

        self.progress_bar.set(
            progress / 100
        )

        self.metrics_label.configure(

            text=(

                f"Processed: "

                f"{self.operation_state.completed_operations}"

                f" / "

                f"{self.operation_state.total_operations}"
            )
        )

    # =====================================================
    # TRANSACTION COMPLETE CALLBACK
    # =====================================================

    def on_transaction_complete(self, result):

        self.after(

            0,

            lambda:
            self.display_transaction_results(
                result
            )
        )

    # =====================================================
    # DISPLAY TRANSACTION RESULTS
    # =====================================================

    def display_transaction_results(self, result):

        success = result["success"]

        rollback_log = result["rollback_log"]

        transaction = result["transaction"]

        # =================================================
        # CANCELLATION
        # =================================================

        if self.operation_state.cancel_requested:

            self.results_box.insert(

                "end",

                "\n⚠ Operation Cancelled By User\n"
            )

            self.status_label.configure(
                text="Status: Cancelled"
            )

            return

        # =================================================
        # FAILURE
        # =================================================

        if not success:

            self.status_label.configure(
                text="Status: Transaction Failed"
            )

            self.results_box.insert(

                "end",

                (
                    "\n==================================================\n"
                    "TRANSACTION FAILED\n"
                    "==================================================\n\n"
                )
            )

            self.results_box.insert(

                "end",

                (
                    "❌ Transaction integrity failure.\n"
                    "⚠ Automatic rollback executed.\n\n"
                )
            )

            return

        # =================================================
        # SUCCESS
        # =================================================

        self.status_label.configure(
            text="Status: Transaction Committed"
        )

        self.results_box.insert(

            "end",

            (
                "\n==================================================\n"
                "TRANSACTION COMMITTED\n"
                "==================================================\n\n"
            )
        )

        for item in rollback_log:

            old_name = Path(
                item["old"]
            ).name

            new_name = Path(
                item["new"]
            ).name

            self.results_box.insert(

                "end",

                (
                    f"✅ {old_name}\n"
                    f"→ {new_name}\n\n"
                )
            )

        self.results_box.insert(

            "end",

            (
                f"\nTransaction ID:\n"
                f"{transaction.transaction_id}\n\n"
            )
        )

        self.results_box.insert(

            "end",

            (
                f"Operations:\n"
                f"{len(rollback_log)}\n\n"
            )
        )

        self.results_box.insert(

            "end",

            (
                "✅ Predictive atomic "
                "transaction completed successfully.\n"
            )
        )

    # =====================================================
    # UNDO LAST TRANSACTION
    # =====================================================

    def undo_last_rename(self):

        rollback_log = load_rollback()

        if not rollback_log:

            self.results_box.insert(

                "end",

                "\n❌ No rollback history found.\n"
            )

            return

        self.status_label.configure(
            text="Status: Rolling Back..."
        )

        self.results_box.insert(

            "end",

            "\n↩ Starting rollback...\n\n"
        )

        results = undo_renames(
            rollback_log
        )

        success_count = 0

        failed_count = 0

        for result in results:

            if result["status"] == "success":

                success_count += 1

                self.results_box.insert(

                    "end",

                    (
                        f"✅ Restored:\n"
                        f"{result['restored']}\n\n"
                    )
                )

            else:

                failed_count += 1

                self.results_box.insert(

                    "end",

                    (
                        "❌ Rollback Failed:\n"
                        f"{result['reason']}\n\n"
                    )
                )

        clear_rollback()

        self.status_label.configure(
            text="Status: Rollback Complete"
        )

        self.results_box.insert(

            "end",

            (
                "\n🎯 Rollback Complete\n"

                f"Success: {success_count}\n"

                f"Failed: {failed_count}\n"
            )
        )

    # =====================================================
    # CANCEL OPERATION
    # =====================================================

    def cancel_operation(self):

        self.operation_state.request_cancel()

        self.status_label.configure(
            text="Status: Cancellation Requested..."
        )

        self.results_box.insert(

            "end",

            (
                "\n⚠ User requested "
                "operation cancellation.\n"
            )
        )


# =========================================================
# APPLICATION ENTRY
# =========================================================

if __name__ == "__main__":

    app = SafeRenameApp()

    app.mainloop()