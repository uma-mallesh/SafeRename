import customtkinter as ctk

from tkinter import filedialog
from pathlib import Path

from core.scanner.file_scanner import scan_folder

from core.rename_engine.rename_manager import safe_rename
from core.rename_engine.collision_handler import resolve_collision

from core.rename_engine.rollback_manager import (
    save_rollback,
    load_rollback,
    clear_rollback
)

from core.rename_engine.undo_engine import undo_renames
from core.rename_engine.transaction_validator import (
    validate_transaction
)

from core.rename_engine.transaction_queue import (
    TransactionQueue
)


# Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SafeRenameApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window
        self.title("SafeRename")
        self.geometry("950x700")

        # Store scan results
        self.results = []

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="SafeRename 🚀",
            font=("Arial", 32, "bold")
        )

        self.title_label.pack(pady=20)

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Offline Unicode Filename Sanitizer",
            font=("Arial", 16)
        )

        self.subtitle_label.pack(pady=5)

        # Scan Button
        self.scan_button = ctk.CTkButton(
            self,
            text="Select Folder & Scan",
            command=self.select_folder,
            width=250,
            height=40
        )

        self.scan_button.pack(pady=10)

        # Rename Button
        self.rename_button = ctk.CTkButton(
            self,
            text="Rename All",
            command=self.rename_files,
            fg_color="darkgreen",
            hover_color="green",
            width=250,
            height=40
        )

        self.rename_button.pack(pady=10)

        # Undo Button
        self.undo_button = ctk.CTkButton(
            self,
            text="Undo Last Rename",
            command=self.undo_last_rename,
            fg_color="darkred",
            hover_color="red",
            width=250,
            height=40
        )

        self.undo_button.pack(pady=10)

        # Results Box
        self.results_box = ctk.CTkTextbox(
            self,
            width=850,
            height=450,
            font=("Consolas", 14)
        )

        self.results_box.pack(pady=20)
        self.transaction_queue = TransactionQueue()

    # -----------------------------------
    # SELECT + SCAN
    # -----------------------------------

    def select_folder(self):

        folder_selected = filedialog.askdirectory()

        if not folder_selected:
            return

        self.results_box.delete("1.0", "end")

        self.results_box.insert(
            "end",
            f"Scanning Folder:\n{folder_selected}\n\n"
        )

        self.results = scan_folder(folder_selected)

        if not self.results:

            self.results_box.insert(
                "end",
                "✅ No problematic filenames found."
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
                f"{'-'*60}\n"
            )

            self.results_box.insert(
                "end",
                preview_text
            )

    # -----------------------------------
    # RENAME ENGINE
    # -----------------------------------

    def rename_files(self):

        if not self.results:

            self.results_box.insert(
                "end",
                "\nNo scan results available.\n"
            )

            return

        rename_log = []

        self.results_box.insert(
            "end",
            "\n\nStarting rename process...\n\n"
        )

        for item in self.results:

            try:

                original_path = item["path"]

                original_file = Path(original_path)

                directory = original_file.parent

                cleaned_name = item["cleaned"]

                # Collision-safe filename
                safe_name = resolve_collision(
                    directory,
                    cleaned_name
                )
                # Validate transaction
                issues = validate_transaction(
                    original_path,
                    safe_name
                )

                if issues:

                    self.results_box.insert(
                        "end",
                        f"❌ Validation Failed:\n"
                        f"{item['original']}\n"
                    )

                    for issue in issues:

                        self.results_box.insert(
                            "end",
                            f"   - {issue}\n"
                        )

                    self.results_box.insert(
                        "end",
                        "\n"
                    )

                    continue
                

               
                result = safe_rename(
                    original_path,
                    safe_name
                )

                rename_log.append(result)

                self.results_box.insert(
                    "end",
                    f"✅ Renamed:\n"
                    f"{original_file.name}\n"
                    f"→ {safe_name}\n\n"
                )

            except Exception as error:

                self.results_box.insert(
                    "end",
                    f"❌ Failed:\n"
                    f"{item['original']}\n"
                    f"{error}\n\n"
                )

        # Save rollback history
        save_rollback(rename_log)

        self.results_box.insert(
            "end",
            "\n✅ Rename operation completed.\n"
            "Rollback history saved.\n"
        )
        self.transaction_queue.add({
            "original": original_path,
            "safe_name": safe_name
        })
        self.results_box.insert(
            "end",
            f"\nTransaction Queue Processed:\n"
            f"{self.transaction_queue.count()} operations\n"
        )

    # -----------------------------------
    # UNDO ENGINE
    # -----------------------------------

    def undo_last_rename(self):

        rollback_log = load_rollback()

        if not rollback_log:

            self.results_box.insert(
                "end",
                "\nNo rollback history found.\n"
            )

            return

        self.results_box.insert(
            "end",
            "\nStarting rollback...\n\n"
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

        self.results_box.insert(
            "end",
            f"\nRollback Complete.\n"
            f"Success: {success_count}\n"
            f"Failed: {failed_count}\n"
        )


# -----------------------------------
# APP ENTRY
# -----------------------------------

if __name__ == "__main__":

    app = SafeRenameApp()

    app.mainloop()