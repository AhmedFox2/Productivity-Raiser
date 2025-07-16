import os
import keyboard
import customtkinter as ctk
from pathlib import Path
from home import HomePage
from password_window import PasswordWindow
from PIL import Image
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

        self.bind("<F12>", lambda e: self.exit_btn.pack(side="right", padx=20))

        keyboard.block_key("tab")
        self.bind("<Alt-F4>", lambda e: "break")
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        self.content_frame = ctk.CTkFrame(self,fg_color="transparent")
        self.content_frame.pack(expand=True,fill="both")

        self.home_page = HomePage(self.content_frame)
        self.home_page.pack(expand=True, fill="both")

        # إنشاء الإطار السفلي
        self.main_frame = ctk.CTkFrame(self, width=700, height=70, fg_color="#2d2d2d", corner_radius=15)
        self.main_frame.pack(side="bottom", pady=(0, 20))  # مسافة 20 من الأسفل
        self.home_icon = Image.open(f"{icons_folder}/Home_light.svg")
        self.home_button = ctk.CTkButton(self.main_frame, text="", command=self.clear_ui,fg_color="#4a9eff", hover_color="#2d7bdb",text_color="white", corner_radius=12, width=120,font=("Tajawal", 14, "bold"),image=ctk.CTkImage(light_image=self.home_icon,dark_image=self.home_button,size=(64,64)))
        self.home_button.pack(side="left",padx=10,pady=10)

        self.exit_btn = ctk.CTkButton(self, text="خروج آمن",
                                      command=self.ask_password,
                                      fg_color="#ff4444", hover_color="#cc0000",
                                      text_color="white", corner_radius=12, width=120,
                                      font=("Tajawal", 14, "bold"))
        self.exit_btn.pack_forget()

        self.set_dark_theme()
    def clear_ui(self):
        """Clear the current UI elements."""
        for widget in self.content_frame.winfo_children():
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
        self.home_page.update_button_colors("#e2e4e6")
        self.main_frame.configure(fg_color=header_color)  # نفس لون الهيدر

    def ask_password(self):
        PasswordWindow(self)
if __name__ == "__main__":
    app = App()
    app.mainloop()
