import tkinter as tk
from lib.theme import PRIMARY_COLOR
from ProfileWindow import ProfileWindow


class WelcomeWindow(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        container = tk.Frame(self)
        container.config(bg=self.backgroundColor, padx=20, pady=20)
        # container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        container.pack(expand=True)

        tk.Label(
            container,
            text="WELCOME TO SMART STUDY",
            bg=self.backgroundColor,
            font=("Arial", 24, "bold"),
        ).pack(pady=10)

        summary = (
            "Smart Study is an app to effectively manage, track and study materials.\n\n"
            "Materials for each course are uploaded, and a timetable for study is created at account creation for the user."
        )
        tk.Label(
            container,
            text=summary,
            bg=self.backgroundColor,
            font=("Arial", 14),
            wraplength=400,
            justify=tk.LEFT,
        ).pack(pady=10)

        tk.Button(
            container,
            text="GET STARTED",
            bg=PRIMARY_COLOR,
            fg="white",
            command=self.get_started,
        ).pack(pady=20)

        # self.pack(fill=tk.BOTH, expand=True)

    def get_started(self):
        # e.g., navigate to ProfileWindow
        self.master.master.show_page(ProfileWindow.__name__)
