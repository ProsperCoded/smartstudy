import tkinter as tk
from pages.ProfileWindow import ProfileWindow
from pages.Welcome import WelcomeWindow
from pages.Timetable import Timetable
from pages.UploadMaterials import UploadMaterials

"""
Main module for the SmartStudy application.

This module initializes the main window using the customtkinter library.
"""

pages = [WelcomeWindow, ProfileWindow, Timetable, UploadMaterials]


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

        # * initialize and store all pages
        for page in pages:
            initializedPage = page(parent=container)
            initializedPage.grid(row=0, column=0, sticky="nsew")
            self.pages[page.__name__] = initializedPage

    def show_page(self, page_name):
        self.pages[page_name].tkraise()


# START APPLICATION
app = App()
app.show_page(UploadMaterials.__name__)
app.mainloop()
