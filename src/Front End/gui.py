import os
import json
import subprocess
import customtkinter as ctk
import keyboard
import icoextract
from PIL import Image

def extract_icon_from_exe(exe_path,app_name=None):
    try:
        icoextract.IconExtractor(exe_path).export_icon(program_path.removesuffix("Front End") + "\\assets\\icons\\"+app_name + ".ico")
        return Image.open(program_path.removesuffix("Front End") + "\\assets\\icons\\"+app_name + ".ico")
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

        ctk_img = ctk.CTkImage(light_image=Image.open(program_path.removesuffix("Front End") + "\\assets\\icons\\"+app_name + ".ico"), dark_image=Image.open(program_path.removesuffix("Front End") + "\\assets\\icons\\"+app_name + ".ico"), size=(64, 64))

        btn = ctk.CTkButton(
            content_frame,
            image=ctk_img,
            text="",
            width=80,
            height=80,
            fg_color="transparent",
            hover_color="#444",
            corner_radius=20,
            command=lambda p=path: run_app(p)
        )

        row = i // 5
        col = i % 5
        btn.grid(row=row, column=col, padx=20, pady=20)

# إعداد المظهر
ctk.set_appearance_mode("light")  # وضع فاتح
ctk.set_default_color_theme("green")  # اللون الأساسي أخضر

# النافذة الرئيسية
app = ctk.CTk()
app.title("Study Mode Launcher")
app.attributes("-fullscreen", True)
app.resizable(False, False)
app.attributes("-topmost", True)

# منع Tab و Alt+F4
keyboard.block_key("tab")
app.bind("<Alt-F4>", lambda e: "break")
app.protocol("WM_DELETE_WINDOW", lambda: None)

# إطار رأس الصفحة
header_frame = ctk.CTkFrame(app, corner_radius=20, fg_color="#e6f4ea")
header_frame.pack(fill="x", pady=20, padx=40)

welcome = ctk.CTkLabel(
    header_frame,
    text="أهلاً بك في وضع الدراسة",
    font=("Segoe UI", 34, "bold"),
    text_color="#2e7d32"
)
welcome.pack(pady=10)

info = ctk.CTkLabel(
    header_frame,
    text="لإغلاق، اضغط F12 وأدخل كلمة المرور",
    font=("Segoe UI", 18)
)
info.pack(pady=(0,10))

# إظهار زر خروج عند الضغط على F12
exit_btn = ctk.CTkButton(
    header_frame,
    text="خروج آمن",
    command=lambda: ask_password(),
    fg_color="#d32f2f",
    hover_color="#b71c1c",
    text_color="white",
    corner_radius=12,
    width=120
)
exit_btn.pack(side="right", padx=20)
exit_btn.pack_forget()

app.bind("<F12>", lambda e: exit_btn.pack(side="right", padx=20))

# إطار لعرض البرامج
content_frame = ctk.CTkScrollableFrame(
    app,
    width=1400,
    height=700,
    fg_color="transparent",
    corner_radius=20,
    scrollbar_button_color="#ebebeb"
)
content_frame.pack(pady=30)

# إضافة أزرار التطبيقات بشكل Grid

show_allowed_apps()

# نافذة كلمة المرور

def ask_password():
    pwd_win = ctk.CTkToplevel(app)
    pwd_win.title("كلمة المرور")
    pwd_win.geometry("320x180")
    pwd_win.attributes("-topmost", True)
    pwd_win.transient(app)
    pwd_win.grab_set()

    lbl = ctk.CTkLabel(pwd_win, text="أدخل كلمة المرور:", font=("Segoe UI", 16))
    lbl.pack(pady=(20,10))

    entry = ctk.CTkEntry(pwd_win, show="*", font=("Segoe UI", 16), width=240)
    entry.pack(pady=5)

    def check():
        if entry.get() == "1234":
            app.destroy()
        else:
            ctk.CTkLabel(
                pwd_win,
                text="كلمة السر خاطئة!",
                text_color="#d32f2f",
                font=("Segoe UI", 14)
            ).pack(pady=5)

    btn = ctk.CTkButton(pwd_win, text="تأكيد", command=check, width=100, corner_radius=12)
    btn.pack(pady=15)

# تشغيل الواجهة
app.mainloop()