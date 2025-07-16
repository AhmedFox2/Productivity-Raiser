import customtkinter as ctk
import json
from pathlib import Path

src = Path(__file__).resolve().parent.parent
icons_folder = src / "assets" / "icons"
json_path = src / "assets" / "database"
font_path = src / "assets" / "fonts" / "Cairo-Regular.ttf"

def load_json_file():
    try:
        with open(f"{json_path}/tasks.json" ,"r") as file:
            return json.load(file)
    except Exception as e:
        print(e)

def save_json_file(data):
    try:
        with open(f"{json_path}/tasks.json","w") as file:
            return json.dump(file,data,indent=4)
    except Exception as e:
        print(e)

class ToDoList(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master,fg_color="transparent")
        self.parent = master
        self.build_ui()

    def build_ui(self):
        self.gg = ctk.CTkLabel(self,text="hih")
        self.gg.pack()