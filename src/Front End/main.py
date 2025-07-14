import os
import keyboard
import customtkinter as ctk
from pathlib import Path
from home import HomePage

# مسارات
src = Path(__file__).resolve().parent.parent
icons_folder = src / "assets" / "icons"
json_path = src / "assets" / "database"
font_path = src / "assets" / "fonts" / "Cairo-Regular.ttf"

# التطبيق الأساسي
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Study Mode Launcher")
        self.attributes("-fullscreen", True)
        self.resizable(False, False)
        self.attributes("-topmost", True)

        keyboard.block_key("tab")
        self.bind("<Alt-F4>", lambda e: "break")
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        self.home_page = HomePage(self)
        self.home_page.pack(expand=True, fill="both")

        self.set_dark_theme()

        self.main_frame = ctk.CTkFrame(self.home_page,width=700,height=70)
        self.main_frame.pack()
    def clear_ui(self):
        """Clear the current UI elements."""
        for widget in self.winfo_children():
            widget.destroy()

    def set_dark_theme(self):
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#1a1a1a")
        self.home_page.header_frame.configure(fg_color="#2d2d2d")
        self.home_page.content_frame.configure(fg_color="#2d2d2d")
        self.home_page.welcome.configure(text_color="#4a9eff")
        self.home_page.info.configure(text_color="#8b8b8b")
        self.home_page.theme_btn.configure(text="☀", fg_color="#4a9eff", hover_color="#2d7bdb")
        self.home_page.exit_btn.configure(fg_color="#ff4444", hover_color="#cc0000", text_color="white")
        self.home_page.update_button_colors("#363636")

    def set_light_theme(self):
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#f7fafc")
        self.home_page.header_frame.configure(fg_color="#e3f2fd")
        self.home_page.content_frame.configure(fg_color="#f7fafc")
        self.home_page.welcome.configure(text_color="#1976d2")
        self.home_page.info.configure(text_color="#607d8b")
        self.home_page.theme_btn.configure(text="☾", fg_color="#1976d2", hover_color="#1565c0")
        self.home_page.exit_btn.configure(fg_color="#e53935", hover_color="#b71c1c", text_color="white")
        self.home_page.update_button_colors("#e2e4e6")


if __name__ == "__main__":
    app = App()
    app.mainloop()
