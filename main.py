# import tkinter as tk
import customtkinter as ctk
import pages.UserProfile as UserProfile

"""
Main module for the SmartStudy application.

This module initializes the main window using the customtkinter library.
"""


# CONFIGURATIONS
root = ctk.CTk()
root.title("SmartStudy")
root.geometry("1000x800")

# ------------------ WIDGETS ------------------
userprofile = UserProfile.ProfileWindow(root)


# ------------------ WIDGETS ------------------

# START APPLICATION
root.mainloop()
