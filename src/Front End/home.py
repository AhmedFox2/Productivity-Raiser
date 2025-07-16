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

appearance_mode = ["dark"]

class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.parent = master
        self.build_ui()

    def build_ui(self):
        self.cairo_font = ctk.CTkFont(family=str(font_path), size=30)
        self.header_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#2d2d2d")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.theme_btn = ctk.CTkButton(self.header_frame, text="☀", width=50, height=40,
                                       fg_color="#4a9eff", hover_color="#2d7bdb",
                                       text_color="white", font=("Segoe UI", 20, "bold"),
                                       corner_radius=12, command=self.toggle_appearance)
        self.theme_btn.pack(side="left", padx=10)

        self.welcome = ctk.CTkLabel(self.header_frame, text="أهلاً بك في وضع الدراسة",
                                    font=("Tajawal", 34, "bold"), text_color="#4a9eff")
        self.welcome.pack(pady=10)

        self.info = ctk.CTkLabel(self.header_frame, text="لإغلاق، اضغط F12 وأدخل كلمة المرور",
                                 font=("Tajawal", 18), text_color="#8b8b8b")
        self.info.pack(pady=(0, 10))

        # إنشاء إطار وسطي للمحتوى
        self.middle_container = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_container.pack(expand=True, fill="both")
        
        # إطار المحتوى الرئيسي مع تكيف تلقائي للحجم
        self.content_frame = ctk.CTkScrollableFrame(
            self.middle_container,
            fg_color="#2d2d2d",
            corner_radius=20,
            scrollbar_button_color="#404040"
        )
        
        self.show_allowed_apps()
        self.set_dark_theme()

    def show_allowed_apps(self):
        apps = load_allowed_apps()
        
        # حساب عدد الأعمدة بناءً على عرض النافذة
        window_width = self.winfo_screenwidth()
        app_width = 140  # عرض كل تطبيق مع الهوامش
        max_columns = min(max(3, window_width // app_width), 7)  # على الأقل 3 وحد أقصى 7 أعمدة
        
        # حساب الأبعاد المطلوبة للمحتوى
        num_apps = len(apps)
        num_rows = (num_apps + max_columns - 1) // max_columns
        content_width = (app_width + 50) * max_columns  # 50 للهوامش
        content_height = (140 + 50) * num_rows  # 140 لارتفاع كل تطبيق، 50 للهوامش
        
        # ضبط حجم إطار المحتوى
        self.content_frame.configure(width=content_width, height=min(content_height, 800))
        
        # وضع إطار المحتوى في المنتصف
        self.content_frame.pack(expand=True, pady=(20, 20))
        
        for i, path in enumerate(apps):
            exe_name = os.path.basename(path)
            app_name = exe_name.removesuffix(".exe")

            icon_path = icons_folder / f"{app_name}.ico"
            if not icon_path.exists():
                extract_icon_from_exe(path, app_name)

            icon_img = Image.open(icon_path)
            ctk_img = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(64, 64))

            app_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")

            btn = ctk.CTkButton(app_frame, image=ctk_img, text="", width=90, height=90,
                                fg_color="#363636", hover_color="#4a9eff", corner_radius=15,
                                command=lambda p=path: self.run_app(p))
            btn.pack(pady=2)  # تقليل المسافة الرأسية

            label = ctk.CTkLabel(app_frame, text=app_name, font=self.cairo_font, text_color="#8b8b8b")
            label.pack()

            row = i // max_columns
            col = i % max_columns
            app_frame.grid(row=row, column=col, padx=15, pady=15)  # تقليل المسافات بين التطبيقات
            
            # إضافة وزن متساوٍ للأعمدة لتوسيطها
            self.content_frame.grid_columnconfigure(col, weight=1)
            
        # إضافة وزن متساوٍ للصفوف
        for row in range((len(apps) + max_columns - 1) // max_columns):
            self.content_frame.grid_rowconfigure(row, weight=1)

    def toggle_appearance(self):
        if appearance_mode[0] == "dark":
            appearance_mode[0] = "light"
            self.set_light_theme()
        else:
            appearance_mode[0] = "dark"
            self.set_dark_theme()

    def update_button_colors(self, color):
        for widget in self.content_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(fg_color=color)
    
    def run_app(self, path):
        self.parent.attributes("-topmost", False)
        subprocess.Popen(path)
        self.parent.destroy()

    def set_dark_theme(self):
        ctk.set_appearance_mode("dark")
        bg_color = "#1a1a1a"
        header_color = "#2d2d2d"
        self.configure(fg_color=bg_color)
        self.header_frame.configure(fg_color=header_color)
        self.content_frame.configure(fg_color=bg_color, scrollbar_button_color=bg_color)
        self.welcome.configure(text_color="#4a9eff")
        self.info.configure(text_color="#8b8b8b")
        self.theme_btn.configure(text="☀", fg_color="#4a9eff", hover_color="#2d7bdb")
        self.update_button_colors("#363636")

    def set_light_theme(self):
        ctk.set_appearance_mode("light")
        bg_color = "#f7fafc"
        header_color = "#e3f2fd"
        self.configure(fg_color=bg_color)
        self.header_frame.configure(fg_color=header_color)
        self.content_frame.configure(fg_color=bg_color, scrollbar_button_color=bg_color)
        self.welcome.configure(text_color="#1976d2")
        self.info.configure(text_color="#607d8b")
        self.theme_btn.configure(text="☾", fg_color="#1976d2", hover_color="#1565c0")
        self.update_button_colors("#e2e4e6")
