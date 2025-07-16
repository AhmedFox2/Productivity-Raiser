import os
import keyboard
import customtkinter as ctk
from pathlib import Path
from home import HomePage
from password_window import PasswordWindow
from PIL import Image
from to_do_list import ToDoList
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

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both")

        self.pages = {}         # هنا نخزن الصفحات
        self.current_page = None

        self.set_page("home")

        # الشريط السفلي
        self.main_frame = ctk.CTkFrame(self, width=700, height=70, fg_color="#2d2d2d", corner_radius=15)
        self.main_frame.pack(side="bottom", pady=(0, 20))

        self.home_icon = Image.open(f"{icons_folder}/home_dark.png")
        self.todolist_icon = Image.open(f"{icons_folder}/add_light.png")

        self.create_nav_button(self.home_icon, "home").pack(side="left", padx=10, pady=10)
        self.create_nav_button(self.todolist_icon, "tasks").pack(side="left", padx=10, pady=10)

        self.exit_btn = ctk.CTkButton(self, text="خروج آمن", command=self.ask_password,
                                      fg_color="#ff4444", hover_color="#cc0000",
                                      text_color="white", corner_radius=12, width=120,
                                      font=("Tajawal", 14, "bold"))
        self.exit_btn.pack_forget()

    def create_nav_button(self, icon, page_name):
        return ctk.CTkButton(self.main_frame, text="", command=lambda: self.set_page(page_name),
                             fg_color="transparent", hover_color="#3f4347",
                             text_color="white", corner_radius=12, width=120,
                             font=("Tajawal", 14, "bold"),
                             image=ctk.CTkImage(light_image=icon, dark_image=icon, size=(64, 64)))

    def set_page(self, page_name):
        pages_map = {"home": HomePage, "tasks": ToDoList}

        if self.current_page == page_name:
            return

        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].pack_forget()

        if page_name in self.pages:
            page = self.pages[page_name]
            page.pack(expand=True, fill="both")
        else:
            page = pages_map[page_name](master=self.content_frame)
            page.pack(expand=True, fill="both")
            self.pages[page_name] = page

        self.current_page = page_name


    def ask_password(self):
        PasswordWindow(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
