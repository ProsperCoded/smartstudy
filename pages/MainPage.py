import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import os
from lib.theme import PRIMARY_COLOR
from lib.utils import load_from_json


class MainPage(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Load timetable
        self.timetable = load_from_json("store/timetable.json")
        try:
            self.materials_df = pd.read_excel("store/materials.xlsx")
        except FileNotFoundError:
            self.materials_df = pd.DataFrame(columns=["course", "material"])

        self.create_menu()
        self.create_ui()

    def create_menu(self):
        menubar = tk.Menu(self.parent)
        self.parent.master.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=file_menu)
        file_menu.add_command(
            label="Timetable", command=lambda: self.navigate_to("Timetable")
        )
        file_menu.add_command(
            label="Upload Materials",
            command=lambda: self.navigate_to("UploadMaterials"),
        )

        # Profile menu
        profile_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Profile", menu=profile_menu)
        profile_menu.add_command(
            label="Change Profile", command=lambda: self.navigate_to("ProfileWindow")
        )

    def create_ui(self):
        container = tk.Frame(self, bg=self.backgroundColor)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        tk.Label(
            container,
            text="SMART STUDY DASHBOARD",
            font=("Arial", 24, "bold"),
            bg=self.backgroundColor,
        ).pack(pady=20)

        # Notifications Section
        notification_frame = tk.LabelFrame(
            container, text="Notifications", bg=self.backgroundColor
        )
        notification_frame.pack(fill=tk.X, pady=10)
        self.show_unengaged_courses(notification_frame)

        # Materials Section
        materials_frame = tk.LabelFrame(
            container, text="Course Materials", bg=self.backgroundColor
        )
        materials_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.show_materials(materials_frame)

        # Main CTA Button
        self.create_main_cta(container)

    def show_unengaged_courses(self, parent):
        # Placeholder for tracking logic - will need to be implemented
        unengaged_courses = self.get_unengaged_courses()
        if not unengaged_courses:
            tk.Label(
                parent,
                text="You're up to date with all courses!",
                bg=self.backgroundColor,
            ).pack(pady=10)
        else:
            for course in unengaged_courses:
                tk.Label(
                    parent, text=f"⚠️ {course} needs attention", bg=self.backgroundColor
                ).pack(anchor="w")

    def show_materials(self, parent):
        for _, row in self.materials_df.iterrows():
            frame = tk.Frame(parent, bg=self.backgroundColor)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, text=row["course"], bg=self.backgroundColor).pack(
                side=tk.LEFT, padx=5
            )

            tk.Button(
                frame,
                text="START STUDY",
                command=lambda m=row["material"]: self.open_material(m),
                bg=PRIMARY_COLOR,
                fg="white",
            ).pack(side=tk.RIGHT, padx=5)

    def create_main_cta(self, parent):
        current_day = datetime.now().strftime("%A")
        todays_courses = self.timetable.get(current_day, [])

        if todays_courses:
            tk.Button(
                parent,
                text=f"START TODAY'S STUDY - {', '.join(todays_courses)}",
                command=self.start_todays_study,
                bg=PRIMARY_COLOR,
                fg="white",
                font=("Arial", 12, "bold"),
            ).pack(pady=20)
        else:
            tk.Label(
                parent, text="No courses scheduled for today", bg=self.backgroundColor
            ).pack(pady=20)

    def navigate_to(self, page_name):
        self.parent.master.show_page(page_name)

    def get_unengaged_courses(self):
        # Placeholder - implement tracking logic
        return []

    def open_material(self, material_path):
        if os.path.exists(material_path):
            os.startfile(material_path)
        else:
            messagebox.showerror("Error", "Material file not found!")

    def start_todays_study(self):
        current_day = datetime.now().strftime("%A")
        todays_courses = self.timetable.get(current_day, [])

        if todays_courses:
            course = todays_courses[0]  # Take first course
            material = self.materials_df[self.materials_df["course"] == course]

            if not material.empty:
                self.open_material(material.iloc[0]["material"])
            else:
                messagebox.showinfo("Note", "No material found for today's course")
