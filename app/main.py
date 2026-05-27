import customtkinter as ctk

from tkinter import filedialog

from core.scanner.file_scanner import scan_folder
from core.rename_engine.rename_manager import safe_rename
from core.rename_engine.rollback_manager import save_rollback
from core.rename_engine.collision_handler import resolve_collision
from pathlib import Path


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SafeRenameApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SafeRename")
        self.geometry("900x600")

        # Title
        title = ctk.CTkLabel(
            self,
            text="SafeRename 🚀",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=20)

        # Scan Button
        scan_button = ctk.CTkButton(
            self,
            text="Select Folder & Scan",
            command=self.select_folder
        )

        scan_button.pack(pady=20)

        # Results Box
        self.results_box = ctk.CTkTextbox(
            self,
            width=800,
            height=400
        )

        self.results_box.pack(pady=20)
        self.rename_button = ctk.CTkButton(
            self,
            text="Rename All",
            command=self.rename_files
        )

        self.rename_button.pack(pady=10)
        

    def select_folder(self):

        folder_selected = filedialog.askdirectory()

        if not folder_selected:
            return

        self.results_box.delete("1.0", "end")

        self.results_box.insert(
            "end",
            f"Scanning:\n{folder_selected}\n\n"
        )

        self.results = scan_folder(folder_selected)

        if not self.results:

            self.results_box.insert(
                "end",
                "✅ No emoji filenames found."
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
             f"{'-'*50}\n"
            )

            self.results_box.insert(
                "end",
                preview_text
            )

    def rename_files(self):

        if not hasattr(self, 'results'):
            return

        rename_log = []

        self.results_box.insert(
            "end",
            "\n\nStarting rename process...\n"
        )

        for item in self.results:

            try:

                original_path = item["path"]

                original_file = Path(original_path)

                directory = original_file.parent

                cleaned_name = item["cleaned"]

                # Resolve collisions
                safe_name = resolve_collision(
                    directory,
                    cleaned_name
                )

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

        save_rollback(rename_log)

        self.results_box.insert(
            "end",
            "\nRollback history saved.\n"
        )
            

if __name__ == "__main__":
    app = SafeRenameApp()
    app.mainloop()