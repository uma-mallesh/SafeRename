import customtkinter as ctk

from tkinter import filedialog

from core.scanner.file_scanner import scan_folder


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

    def select_folder(self):

        folder_selected = filedialog.askdirectory()

        if not folder_selected:
            return

        self.results_box.delete("1.0", "end")

        self.results_box.insert(
            "end",
            f"Scanning:\n{folder_selected}\n\n"
        )

        results = scan_folder(folder_selected)

        if not results:

            self.results_box.insert(
                "end",
                "✅ No emoji filenames found."
            )

            return

        self.results_box.insert(
            "end",
            f"⚠ Found {len(results)} problematic files:\n\n"
        )

        for item in results:

            self.results_box.insert(
                "end",
                f"{item['name']}\n"
            )


if __name__ == "__main__":
    app = SafeRenameApp()
    app.mainloop()