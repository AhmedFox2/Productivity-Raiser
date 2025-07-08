import os
import json
import subprocess
import customtkinter as ctk
import keyboard
import icoextract
from PIL import Image

def extract_icon_from_exe(exe_path,app_name=None):
    try:
        icoextract.IconExtractor(exe_path).export_icon(program_path.removesuffix("Front End") + "assets\\icons\\"+app_name + ".ico")
        return Image.open(program_path.removesuffix("Front End") + "assets\\icons\\"+app_name + ".ico")
    except icoextract.NoIconsAvailableError:
        print(f"لا توجد أيقونات متاحة في {exe_path}")
        return None
    

program_path = os.path.dirname(__file__)

# تحميل البرامج المسموحة
def load_allowed_apps():
    if not os.path.exists(f"{program_path}/allowed_apps.json"):
        return []
    with open(f"{program_path}/allowed_apps.json", "r") as f:
        return json.load(f)

# تشغيل البرنامج
def run_app(path):
    try:
        app.attributes("-topmost", False)
        subprocess.Popen(path)
        exit()
    except Exception as e:
        print(f"خطأ في تشغيل البرنامج: {e}")

# عرض البرامج المسموحة
def show_allowed_apps():
    apps = load_allowed_apps()
    for i, path in enumerate(apps):
        exe_name = os.path.basename(path)
        app_name = exe_name.removesuffix(".exe")
        if not os.path.exists(program_path + "/assets/icons/"+ app_name + ".ico"):
            print(f"البرنامج {app_name} غير موجود في المسار المحدد: {path}")
            icon_img = extract_icon_from_exe(path,app_name)

        ctk_img = ctk.CTkImage(
            light_image=Image.open(program_path.removesuffix("Front End") + "\\assets\\icons\\"+app_name + ".ico"),
            dark_image=Image.open(program_path.removesuffix("Front End") + "\\assets\\icons\\"+app_name + ".ico"),
            size=(64, 64)
        )

        # إطار للأيقونة
        app_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        
        btn = ctk.CTkButton(
            app_frame,
            image=ctk_img,
            text="",
            width=90,
            height=90,
            fg_color="#363636",
            hover_color="#4a9eff",
            corner_radius=15,
            command=lambda p=path: run_app(p)
        )
        btn.pack(pady=5)
        
        # إضافة اسم التطبيق
        app_label = ctk.CTkLabel(
            app_frame,
            text=app_name,
            font=("Tajawal", 12),
            text_color="#8b8b8b"
        )
        app_label.pack()

        row = i // 5
        col = i % 5
        app_frame.grid(row=row, column=col, padx=25, pady=25)

# إعداد المظهر
ctk.set_appearance_mode("dark")  # وضع داكن
ctk.set_default_color_theme("blue")  # اللون الأساسي أزرق

# النافذة الرئيسية
app = ctk.CTk()
app.title("Study Mode Launcher")
app.attributes("-fullscreen", True)
app.resizable(False, False)
app.attributes("-topmost", True)
app.configure(fg_color="#1a1a1a")  # لون خلفية داكن

# منع Tab و Alt+F4
keyboard.block_key("tab")
app.bind("<Alt-F4>", lambda e: "break")
app.protocol("WM_DELETE_WINDOW", lambda: None)

# إطار رأس الصفحة
header_frame = ctk.CTkFrame(app, corner_radius=20, fg_color="#2d2d2d")
header_frame.pack(fill="x", pady=20, padx=40)

welcome = ctk.CTkLabel(
    header_frame,
    text="أهلاً بك في وضع الدراسة",
    font=("Tajawal", 34, "bold"),
    text_color="#4a9eff"
)
welcome.pack(pady=10)

info = ctk.CTkLabel(
    header_frame,
    text="لإغلاق، اضغط F12 وأدخل كلمة المرور",
    font=("Tajawal", 18),
    text_color="#8b8b8b"
)
info.pack(pady=(0,10))

# إظهار زر خروج عند الضغط على F12
exit_btn = ctk.CTkButton(
    header_frame,
    text="خروج آمن",
    command=lambda: ask_password(),
    fg_color="#ff4444",
    hover_color="#cc0000",
    text_color="white",
    corner_radius=12,
    width=120,
    font=("Tajawal", 14, "bold")
)
exit_btn.pack(side="right", padx=20)
exit_btn.pack_forget()

app.bind("<F12>", lambda e: exit_btn.pack(side="right", padx=20))

# إطار لعرض البرامج
content_frame = ctk.CTkScrollableFrame(
    app,
    width=1400,
    height=700,
    fg_color="#2d2d2d",
    corner_radius=20,
    scrollbar_button_color="#404040"
)
content_frame.pack(pady=30)

# إضافة أزرار التطبيقات بشكل Grid

show_allowed_apps()

# نافذة كلمة المرور

def ask_password():
    pwd_win = ctk.CTkToplevel(app)
    pwd_win.title("كلمة المرور")
    pwd_win.geometry("320x200")
    pwd_win.attributes("-topmost", True)
    pwd_win.transient(app)
    pwd_win.grab_set()
    pwd_win.configure(fg_color="#1a1a1a")

    pwd_frame = ctk.CTkFrame(pwd_win, corner_radius=15, fg_color="#2d2d2d")
    pwd_frame.pack(fill="both", expand=True, padx=20, pady=20)

    lbl = ctk.CTkLabel(
        pwd_frame,
        text="أدخل كلمة المرور:",
        font=("Tajawal", 16),
        text_color="#4a9eff"
    )
    lbl.pack(pady=(20,10))

    entry = ctk.CTkEntry(
        pwd_frame,
        show="*",
        font=("Segoe UI", 16),
        width=240,
        fg_color="#363636",
        border_color="#4a9eff",
        text_color="white"
    )
    entry.pack(pady=5)

    def check():
        if entry.get() == "1234":
            app.destroy()
        else:
            error_label = ctk.CTkLabel(
                pwd_frame,
                text="كلمة السر خاطئة!",
                text_color="#ff4444",
                font=("Tajawal", 14)
            )
            error_label.pack(pady=5)
            entry.configure(border_color="#ff4444")
            pwd_win.after(2000, lambda: [error_label.destroy(), entry.configure(border_color="#4a9eff")])

    btn = ctk.CTkButton(
        pwd_frame,
        text="تأكيد",
        command=check,
        width=120,
        height=35,
        corner_radius=12,
        font=("Tajawal", 14, "bold"),
        fg_color="#4a9eff",
        hover_color="#2d7bdb"
    )
    btn.pack(pady=15)

    # تركيز على حقل الإدخال
    entry.focus()
    # ربط مفتاح Enter بزر التأكيد
    pwd_win.bind("<Return>", lambda e: check())

# تشغيل الواجهة
app.mainloop()