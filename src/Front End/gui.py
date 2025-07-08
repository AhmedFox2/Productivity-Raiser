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
appearance_mode = ["dark"]  # قائمة لتخزين الوضع الحالي (قابلة للتغيير داخل الدوال)
ctk.set_appearance_mode(appearance_mode[0])
ctk.set_default_color_theme("blue")  # اللون الأساسي أزرق

# دالة لتبديل الوضع

def toggle_appearance():
    if appearance_mode[0] == "dark":
        ctk.set_appearance_mode("light")
        app.configure(fg_color="#f7fafc")
        header_frame.configure(fg_color="#e3f2fd")
        content_frame.configure(fg_color="#f7fafc")
        welcome.configure(text_color="#1976d2")
        info.configure(text_color="#607d8b")
        theme_btn.configure(text="☾", fg_color="#1976d2", hover_color="#1565c0")
        exit_btn.configure(fg_color="#e53935", hover_color="#b71c1c", text_color="white")
        appearance_mode[0] = "light"
        theme_btn.configure(text="☾")
    else:
        ctk.set_appearance_mode("dark")
        app.configure(fg_color="#1a1a1a")
        header_frame.configure(fg_color="#2d2d2d")
        content_frame.configure(fg_color="#2d2d2d")
        welcome.configure(text_color="#4a9eff")
        info.configure(text_color="#8b8b8b")
        theme_btn.configure(text="☀", fg_color="#4a9eff", hover_color="#2d7bdb")
        exit_btn.configure(fg_color="#ff4444", hover_color="#cc0000", text_color="white")
        appearance_mode[0] = "dark"
        if hasattr(app, "pwd_win") and app.pwd_win.winfo_exists():
            update_password_window_colors("dark")

# دالة لتحديث ألوان نافذة كلمة المرور حسب الوضع

def update_password_window_colors(mode):
    win = app.pwd_win
    frame = win.pwd_frame
    entry = win.pwd_entry
    if mode == "light":
        win.configure(fg_color="#f7fafc")
        frame.configure(fg_color="#e3f2fd")
        entry.configure(fg_color="#ffffff", border_color="#1976d2", text_color="#222")
    else:
        win.configure(fg_color="#1a1a1a")
        frame.configure(fg_color="#2d2d2d")
        entry.configure(fg_color="#363636", border_color="#4a9eff", text_color="white")

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

# زر تبديل الوضع
# ☀ للوضع الفاتح، ☾ للوضع الغامق

theme_btn = ctk.CTkButton(
    header_frame,
    text="☀",
    width=50,
    height=40,
    fg_color="#4a9eff",
    hover_color="#2d7bdb",
    text_color="white",
    font=("Segoe UI", 20, "bold"),
    corner_radius=12,
    command=toggle_appearance
)
theme_btn.pack(side="left", padx=10)

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
    # تخزين النافذة في app
    app.pwd_win = pwd_win

    # تحديد الألوان حسب الوضع الحالي
    if appearance_mode[0] == "light":
        win_bg = "#f7fafc"
        frame_bg = "#e3f2fd"
        entry_bg = "#ffffff"
        border = "#1976d2"
        txt = "#222"
        lbl_color = "#1976d2"
        err_color = "#e53935"
        btn_fg = "#1976d2"
        btn_hover = "#1565c0"
    else:
        win_bg = "#1a1a1a"
        frame_bg = "#2d2d2d"
        entry_bg = "#363636"
        border = "#4a9eff"
        txt = "white"
        lbl_color = "#4a9eff"
        err_color = "#ff4444"
        btn_fg = "#4a9eff"
        btn_hover = "#2d7bdb"

    pwd_win.configure(fg_color=win_bg)
    pwd_frame = ctk.CTkFrame(pwd_win, corner_radius=15, fg_color=frame_bg)
    pwd_frame.pack(fill="both", expand=True, padx=20, pady=20)
    pwd_win.pwd_frame = pwd_frame

    lbl = ctk.CTkLabel(
        pwd_frame,
        text="أدخل كلمة المرور:",
        font=("Tajawal", 16),
        text_color=lbl_color
    )
    lbl.pack(pady=(20,10))

    entry = ctk.CTkEntry(
        pwd_frame,
        show="*",
        font=("Segoe UI", 16),
        width=240,
        fg_color=entry_bg,
        border_color=border,
        text_color=txt
    )
    entry.pack(pady=5)
    pwd_win.pwd_entry = entry

    def check():
        if entry.get() == "1234":
            app.destroy()
        else:
            ctk.CTkLabel(
                pwd_win,
                text="كلمة السر خاطئة!",
                text_color=err_color,
                font=("Tajawal", 14)
            )
            error_label.pack(pady=5)
            entry.configure(border_color=err_color)
            pwd_win.after(2000, lambda: [error_label.destroy(), entry.configure(border_color=border)])

    btn = ctk.CTkButton(
        pwd_frame,
        text="تأكيد",
        command=check,
        width=120,
        height=35,
        corner_radius=12,
        font=("Tajawal", 14, "bold"),
        fg_color=btn_fg,
        hover_color=btn_hover
    )
    btn.pack(pady=15)

    entry.focus()
    pwd_win.bind("<Return>", lambda e: check())
# تشغيل الواجهة
app.mainloop()