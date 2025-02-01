import tkinter as tk
from pages.ProfileWindow import ProfileWindow
from pages.Welcome import WelcomeWindow
from pages.Timetable import Timetable
from pages.UploadMaterials import UploadMaterials
from pages.MainPage import MainPage
from pages.Studying import Studying
from pages.Analysis import Analysis
import os

"""
Main module for the SmartStudy application.

This module initializes the main window using the customtkinter library.
"""

pages = [
    WelcomeWindow,
    ProfileWindow,
    Timetable,
    UploadMaterials,
    MainPage,
    Studying,
    Analysis,
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartStudy")
        self.geometry("1000x800")
        self.pages = {}

        # Container for pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # allow container to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # variable to store what is currently being studied
        self.studying = None
        # * initialize and store all pages
        for page in pages:
            initializedPage = page(parent=container)
            initializedPage.grid(row=0, column=0, sticky="nsew")
            self.pages[page.__name__] = initializedPage

    def show_page(self, page_name):
        self.pages[page_name].tkraise()

    def startTimer(self):
        self.pages[Studying.__name__].update_study_info()
        self.show_page(Studying.__name__)

    def stopTimer(self):
        self.pages[Studying.__name__].stop_timer()

    def stop_study(self):
        if self.studying:
            self.pages[Studying.__name__].stop_timer()
            self.show_page(MainPage.__name__)


# START APPLICATION
app = App()
# checking resources
timetable_path = "store/timetable.json"
materials_path = "store/materials.xlsx"
profile_path = "store/profile.json"
if not os.path.exists(profile_path):
    app.show_page(WelcomeWindow.__name__)
elif not os.path.exists(timetable_path):
    app.show_page(Timetable.__name__)
elif not os.path.exists(materials_path):
    app.show_page(UploadMaterials.__name__)
else:
    app.show_page(MainPage.__name__)
app.mainloop()
