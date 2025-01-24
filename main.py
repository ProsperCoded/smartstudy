import tkinter as tk
from pages.UserProfile import ProfileWindow

"""
Main module for the SmartStudy application.

This module initializes the main window using the customtkinter library.
"""

pages = [ProfileWindow]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartStudy")
        self.geometry("1000x800")
        self.pages = {}

        # * initialize and store all pages
        for page in pages:
            self.pages[page.__name__] = page(self)

    def show_page(self, page_name):
        self.pages[page_name].tkraise()


# START APPLICATION
app = App()
app.show_page(ProfileWindow.__name__)
app.mainloop()
