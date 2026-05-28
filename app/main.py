import customtkinter as ctk

from tkinter import filedialog
from pathlib import Path

# Scanner
from core.scanner.file_scanner import scan_folder

# Rename Engine
from core.rename_engine.rename_manager import safe_rename
from core.rename_engine.collision_handler import resolve_collision

# Rollback
from core.rename_engine.rollback_manager import (
    save_rollback,
    load_rollback,
    clear_rollback
)

# Undo
from core.rename_engine.undo_engine import undo_renames

# Validation
from core.rename_engine.transaction_validator import (
    validate_transaction
)

# Queue
from core.rename_engine.transaction_queue import (
    TransactionQueue
)

# Workers
from core.workers.scan_worker import ScanWorker
from core.workers.rename_worker import RenameWorker


# =========================================================
# THEME CONFIGURATION
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# MAIN APPLICATION
# =========================================================

class SafeRenameApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.title("SafeRename")
        self.geometry("1000x760")

        # -------------------------------------------------
        # APPLICATION STATE
        # -------------------------------------------------

        self.results = []

        self.transaction_queue = TransactionQueue()

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.title_label = ctk.CTkLabel(
            self,
            text="SafeRename 🚀",
            font=("Arial", 34, "bold")
        )

        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Offline Unicode Filename Sanitizer",
            font=("Arial", 16)
        )

        self.subtitle_label.pack(pady=(0, 20))

        # -------------------------------------------------
        # BUTTONS FRAME
        # -------------------------------------------------

        self.button_frame = ctk.CTkFrame(self)

        self.button_frame.pack(pady=10)

        # -------------------------------------------------
        # SCAN BUTTON
        # -------------------------------------------------

        self.scan_button = ctk.CTkButton(
            self.button_frame,
            text="Select Folder & Scan",
            command=self.select_folder,
            width=220,
            height=40
        )

        self.scan_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # -------------------------------------------------
        # RENAME BUTTON
        # -------------------------------------------------

        self.rename_button = ctk.CTkButton(
            self.button_frame,
            text="Rename All",
            command=self.rename_files,
            fg_color="darkgreen",
            hover_color="green",
            width=220,
            height=40
        )

        self.rename_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # -------------------------------------------------
        # UNDO BUTTON
        # -------------------------------------------------

        self.undo_button = ctk.CTkButton(
            self.button_frame,
            text="Undo Last Rename",
            command=self.undo_last_rename,
            fg_color="darkred",
            hover_color="red",
            width=220,
            height=40
        )

        self.undo_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # -------------------------------------------------
        # STATUS LABEL
        # -------------------------------------------------

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Idle",
            font=("Arial", 14)
        )

        self.status_label.pack(pady=5)

        # -------------------------------------------------
        # RESULTS BOX
        # -------------------------------------------------

        self.results_box = ctk.CTkTextbox(
            self,
            width=920,
            height=520,
            font=("Consolas", 14)
        )

        self.results_box.pack(
            pady=20,
            padx=20
        )

    # =====================================================
    # SELECT FOLDER + SCAN
    # =====================================================

    def select_folder(self):

        folder_selected = filedialog.askdirectory()

        if not folder_selected:
            return

        self.results_box.delete("1.0", "end")

        self.results_box.insert(
            "end",
            f"Scanning Folder:\n{folder_selected}\n\n"
        )

        self.status_label.configure(
            text="Status: Scanning..."
        )

        # Background Scan Task
        def scan_task():

            return scan_folder(folder_selected)

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
            f"⚠ Found {len(self.results)} problematic files:\n\n"
        )

        for item in self.results:

            preview_text = (
                f"ORIGINAL:\n"
                f"{item['original']}\n\n"
                f"CLEANED:\n"
                f"{item['cleaned']}\n"
                f"{'-' * 60}\n"
            )

            self.results_box.insert(
                "end",
                preview_text
            )

    # =====================================================
    # START RENAME PROCESS
    # =====================================================

    def rename_files(self):

        if not self.results:

            self.results_box.insert(
                "end",
                "\n❌ No scan results available.\n"
            )

            return

        self.status_label.configure(
            text="Status: Renaming..."
        )

        worker = RenameWorker(
            self.perform_rename_operations,
            self.on_rename_complete
        )

        worker.start()

    # =====================================================
    # PERFORM RENAME OPERATIONS
    # =====================================================

    def perform_rename_operations(self):

        self.transaction_queue.clear()

        rename_log = []

        for item in self.results:

            try:

                original_path = item["path"]

                original_file = Path(original_path)

                directory = original_file.parent

                cleaned_name = item["cleaned"]

                # -----------------------------------------
                # COLLISION HANDLING
                # -----------------------------------------

                safe_name = resolve_collision(
                    directory,
                    cleaned_name
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
                # QUEUE OPERATION
                # -----------------------------------------

                self.transaction_queue.add({
                    "original": original_path,
                    "safe_name": safe_name
                })

                # -----------------------------------------
                # EXECUTE RENAME
                # -----------------------------------------

                result = safe_rename(
                    original_path,
                    safe_name
                )

                rename_log.append(result)

            except Exception:
                pass

        # -----------------------------------------
        # SAVE ROLLBACK
        # -----------------------------------------

        save_rollback(rename_log)

        return rename_log

    # =====================================================
    # RENAME COMPLETE CALLBACK
    # =====================================================

    def on_rename_complete(self, rename_log):

        self.after(
            0,
            lambda: self.display_rename_results(rename_log)
        )

    # =====================================================
    # DISPLAY RENAME RESULTS
    # =====================================================

    def display_rename_results(self, rename_log):

        self.status_label.configure(
            text="Status: Rename Complete"
        )

        self.results_box.insert(
            "end",
            "\n✅ Rename operation completed.\n\n"
        )

        if not rename_log:

            self.results_box.insert(
                "end",
                "No files were renamed.\n"
            )

            return

        for item in rename_log:

            old_name = Path(item["old"]).name
            new_name = Path(item["new"]).name

            self.results_box.insert(
                "end",
                f"✅ Renamed:\n"
                f"{old_name}\n"
                f"→ {new_name}\n\n"
            )

        self.results_box.insert(
            "end",
            f"Processed:\n"
            f"{len(rename_log)} operations\n\n"
        )

        self.results_box.insert(
            "end",
            f"Transaction Queue:\n"
            f"{self.transaction_queue.count()} operations\n"
        )

    # =====================================================
    # UNDO LAST RENAME
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

        results = undo_renames(rollback_log)

        success_count = 0
        failed_count = 0

        for result in results:

            if result["status"] == "success":

                success_count += 1

                self.results_box.insert(
                    "end",
                    f"✅ Restored:\n"
                    f"{result['restored']}\n\n"
                )

            else:

                failed_count += 1

                self.results_box.insert(
                    "end",
                    f"❌ Rollback Failed:\n"
                    f"{result['reason']}\n\n"
                )

        clear_rollback()

        self.status_label.configure(
            text="Status: Rollback Complete"
        )

        self.results_box.insert(
            "end",
            f"\n🎯 Rollback Complete\n"
            f"Success: {success_count}\n"
            f"Failed: {failed_count}\n"
        )


# =========================================================
# APPLICATION ENTRY
# =========================================================

if __name__ == "__main__":

    app = SafeRenameApp()

    app.mainloop()