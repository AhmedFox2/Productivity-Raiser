import customtkinter as ctk

appearance_mode = ["dark"]

class PasswordWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("كلمة المرور")
        self.geometry("320x200")
        self.attributes("-topmost", True)
        self.transient(parent)
        self.grab_set()

        self.mode = appearance_mode[0]
        self.build_ui()

    def build_ui(self):
        mode = self.mode

        colors = {
            "light": {
                "win_bg": "#f7fafc", "frame_bg": "#e3f2fd",
                "entry_bg": "#ffffff", "border": "#1976d2",
                "txt": "#222", "lbl_color": "#1976d2",
                "err_color": "#e53935", "btn_fg": "#1976d2", "btn_hover": "#1565c0"
            },
            "dark": {
                "win_bg": "#1a1a1a", "frame_bg": "#2d2d2d",
                "entry_bg": "#363636", "border": "#4a9eff",
                "txt": "white", "lbl_color": "#4a9eff",
                "err_color": "#ff4444", "btn_fg": "#4a9eff", "btn_hover": "#2d7bdb"
            }
        }[mode]

        self.configure(fg_color=colors["win_bg"])
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color=colors["frame_bg"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        lbl = ctk.CTkLabel(frame, text="أدخل كلمة المرور:", font=("Tajawal", 16), text_color=colors["lbl_color"])
        lbl.pack(pady=(20,10))

        self.entry = ctk.CTkEntry(
            frame, show="*", font=("Segoe UI", 16), width=240,
            fg_color=colors["entry_bg"], border_color=colors["border"],
            text_color=colors["txt"]
        )
        self.entry.pack(pady=5)

        self.error_label = None

        def check():
            if self.entry.get() == "1234":
                self.master.destroy()
            else:
                if self.error_label:
                    self.error_label.destroy()
                self.error_label = ctk.CTkLabel(frame, text="كلمة السر خاطئة!", text_color=colors["err_color"], font=("Tajawal", 14))
                self.error_label.pack(pady=5)
                self.entry.configure(border_color=colors["err_color"])
                self.after(2000, lambda: [self.error_label.destroy(), self.entry.configure(border_color=colors["border"])])

        btn = ctk.CTkButton(frame, text="تأكيد", command=check, width=120, height=35,
                            corner_radius=12, font=("Tajawal", 14, "bold"),
                            fg_color=colors["btn_fg"], hover_color=colors["btn_hover"])
        btn.pack(pady=15)

        self.entry.focus()
        self.bind("<Return>", lambda e: check())