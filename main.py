import tkinter as tk
import pages.UserProfile as UserProfile

"""
Main module for the SmartStudy application.

This module initializes the main window using the customtkinter library.
"""


# CONFIGURATIONS
root = tk.Tk()
root.title("SmartStudy")
root.geometry("1000x800")

# ------------------ WIDGETS ------------------
userprofile = UserProfile.ProfileWindow(root)


# ------------------ WIDGETS ------------------

# START APPLICATION
root.mainloop()
