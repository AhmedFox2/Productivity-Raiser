import customtkinter as ctk
from pathlib import Path
from utitis import load_allowed_apps, extract_icon_from_exe
import os
from PIL import Image
from password_window import PasswordWindow
import subprocess

# مسارات
src = Path(__file__).resolve().parent.parent
icons_folder = src / "assets" / "icons"
json_path = src / "assets" / "database"
font_path = src / "assets" / "fonts" / "Cairo-Regular.ttf"

parentearance_mode = ["dark"]

class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.parent = master
        self.build_ui()

    def build_ui(self):
        self.cairo_font = ctk.CTkFont(family=str(font_path), size=30)

        self.header_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#2d2d2d")
        self.header_frame.pack(fill="x", pady=20, padx=40)

        self.theme_btn = ctk.CTkButton(self.header_frame, text="☀", width=50, height=40,
                                       fg_color="#4a9eff", hover_color="#2d7bdb",
                                       text_color="white", font=("Segoe UI", 20, "bold"),
                                       corner_radius=12, command=self.toggle_parentearance)
        self.theme_btn.pack(side="left", padx=10)

        self.welcome = ctk.CTkLabel(self.header_frame, text="أهلاً بك في وضع الدراسة",
                                    font=("Tajawal", 34, "bold"), text_color="#4a9eff")
        self.welcome.pack(pady=10)

        self.info = ctk.CTkLabel(self.header_frame, text="لإغلاق، اضغط F12 وأدخل كلمة المرور",
                                 font=("Tajawal", 18), text_color="#8b8b8b")
        self.info.pack(pady=(0, 10))

        self.exit_btn = ctk.CTkButton(self.header_frame, text="خروج آمن",
                                      command=self.ask_password,
                                      fg_color="#ff4444", hover_color="#cc0000",
                                      text_color="white", corner_radius=12, width=120,
                                      font=("Tajawal", 14, "bold"))
        self.exit_btn.pack_forget()

        self.parent.bind("<F12>", lambda e: self.exit_btn.pack(side="right", padx=20))

        self.content_frame = ctk.CTkScrollableFrame(self, width=1400, height=700,
                                                    fg_color="#2d2d2d", corner_radius=20,
                                                    scrollbar_button_color="#404040")
        self.content_frame.pack(pady=30)

        self.show_allowed_apps()

    def show_allowed_apps(self):
        apps = load_allowed_apps()
        for i, path in enumerate(apps):
            exe_name = os.path.basename(path)
            app_name = exe_name.removesuffix(".exe")

            icon_path = icons_folder / f"{app_name}.ico"
            if not icon_path.exists():
                extract_icon_from_exe(path, app_name)

            icon_img = Image.open(icon_path)
            ctk_img = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(64, 64))

            parent_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")

            btn = ctk.CTkButton(parent_frame, image=ctk_img, text="", width=90, height=90,
                                fg_color="#363636", hover_color="#4a9eff", corner_radius=15,
                                command=lambda p=path: self.run_app(p))
            btn.pack(pady=5)

            label = ctk.CTkLabel(parent_frame, text=app_name, font=self.cairo_font, text_color="#8b8b8b")
            label.pack()

            row = i // 5
            col = i % 5
            parent_frame.grid(row=row, column=col, padx=25, pady=25)

    def toggle_parentearance(self):
        if parentearance_mode[0] == "dark":
            parentearance_mode[0] = "light"
            self.parent.set_light_theme()
        else:
            parentearance_mode[0] = "dark"
            self.parent.set_dark_theme()

    def ask_password(self):
        PasswordWindow(self.parent)

    def update_button_colors(self, color):
        for widget in self.content_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(fg_color=color)
    
    def run_app(self, path):
        self.parent.attributes("-topmost", False)
        subprocess.Popen(path)
        self.parent.destroy()
