import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk

# إعداد الثيم لـ customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# نافذة التطبيق الأصلية باستخدام ttkbootstrap
main_window = ttk.Window(themename="flatly")
main_window.title("واجهة مختلطة")
main_window.geometry("400x300")

# إطار داخل نافذة ttkbootstrap
frame = ttk.Frame(main_window, padding=20)
frame.pack(fill=BOTH, expand=True)

# عنوان من ttkbootstrap
label = ttk.Label(frame, text="مرحبا بك في الواجهة المختلطة", font=("Arial", 16))
label.pack(pady=(0, 20))

# زر عادي من ttkbootstrap
ttk_button = ttk.Button(frame, text="زر عادي من ttkbootstrap")
ttk_button.pack(pady=10)

# === إدراج customtkinter داخل نافذة فرعية ===
# لإنشاء زر دائري داخل إطار Toplevel

    
def click_circle():
    print("تم الضغط على الزر الدائري")

circular_button = ctk.CTkButton(
        master=main_window,
        text="دائري",
        width=100,
        height=100,
        corner_radius=50,  # يجعل الزر دائريًا تمامًا
        fg_color="green",
        hover_color="#1b8d4a",
        text_color="white",
        command=click_circle
    )
circular_button.place(relx=0.7, rely=0.5, anchor="center")

# زر من ttkbootstrap لفتح الزر الدائري
open_custom_button = ttk.Button(frame, text="عرض زر دائري",bootstyle="success")
open_custom_button.pack(pady=10)

main_window.mainloop()