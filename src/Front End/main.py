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

        # إنشاء الإطار السفلي
        self.main_frame = ctk.CTkFrame(self, width=700, height=70, fg_color="#2d2d2d", corner_radius=15)
        self.main_frame.pack(side="bottom", pady=(0, 20))  # مسافة 20 من الأسفل

        self.home_button = ctk.CTkButton(self.main_frame, text="Home", command=self.home_page.clear_ui,
                                                fg_color="#4a9eff", hover_color="#2d7bdb",
                                                text_color="white", corner_radius=12, width=120,
                                                font=("Tajawal", 14, "bold"))

        self.set_dark_theme()
    def clear_ui(self):
        """Clear the current UI elements."""
        for widget in self.winfo_children():
            widget.destroy()

    def set_dark_theme(self):
        ctk.set_appearance_mode("dark")
        bg_color = "#1a1a1a"
        header_color = "#2d2d2d"
        self.configure(fg_color=bg_color)
        self.home_page.header_frame.configure(fg_color=header_color)
        self.home_page.content_frame.configure(fg_color=bg_color, scrollbar_button_color=bg_color)
        self.home_page.welcome.configure(text_color="#4a9eff")
        self.home_page.info.configure(text_color="#8b8b8b")
        self.home_page.theme_btn.configure(text="☀", fg_color="#4a9eff", hover_color="#2d7bdb")
        self.home_page.exit_btn.configure(fg_color="#ff4444", hover_color="#cc0000", text_color="white")
        self.home_page.update_button_colors("#363636")
        self.main_frame.configure(fg_color=header_color)  # نفس لون الهيدر

    def set_light_theme(self):
        ctk.set_appearance_mode("light")
        bg_color = "#f7fafc"
        header_color = "#e3f2fd"
        self.configure(fg_color=bg_color)
        self.home_page.header_frame.configure(fg_color=header_color)
        self.home_page.content_frame.configure(fg_color=bg_color, scrollbar_button_color=bg_color)
        self.home_page.welcome.configure(text_color="#1976d2")
        self.home_page.info.configure(text_color="#607d8b")
        self.home_page.theme_btn.configure(text="☾", fg_color="#1976d2", hover_color="#1565c0")
        self.home_page.exit_btn.configure(fg_color="#e53935", hover_color="#b71c1c", text_color="white")
        self.home_page.update_button_colors("#e2e4e6")
        self.main_frame.configure(fg_color=header_color)  # نفس لون الهيدر


if __name__ == "__main__":
    app = App()
    app.mainloop()
