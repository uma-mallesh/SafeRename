import customtkinter as ctk

# Configure theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SafeRenameApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SafeRename")
        self.geometry("800x500")

        # Title Label
        title = ctk.CTkLabel(
            self,
            text="SafeRename 🚀",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=40)

        # Subtitle
        subtitle = ctk.CTkLabel(
            self,
            text="Offline Unicode Filename Sanitizer",
            font=("Arial", 16)
        )

        subtitle.pack(pady=10)

        # Button
        button = ctk.CTkButton(
            self,
            text="Hello World",
            command=self.hello_world
        )

        button.pack(pady=30)

    def hello_world(self):
        print("SafeRename is running successfully!")


if __name__ == "__main__":
    app = SafeRenameApp()
    app.mainloop()