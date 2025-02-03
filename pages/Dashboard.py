import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import os
from lib.theme import PRIMARY_COLOR
from lib.utils import load_from_json


class Dashboard(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.reload()
        self.create_menu()
        self.create_ui()

    def reload(self):
        # Load timetable
        self.timetable = load_from_json("store/timetable.json")

        # self.timetable = self.timetable.get(today, [])
        self.profile = load_from_json("store/profile.json")
        try:
            self.materials_df = pd.read_excel("store/materials.xlsx")
        except FileNotFoundError:
            self.materials_df = pd.DataFrame(columns=["course", "material"])
        self.study_buttons = []

        # Refresh UI if it exists
        if hasattr(self, "winfo_children") and self.winfo_children():
            for widget in self.winfo_children():
                widget.destroy()
            self.create_ui()

    def create_menu(self):
        menubar = tk.Menu(self.parent)
        self.parent.master.config(menu=menubar)

        # Home Menu
        home_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Home", menu=home_menu)
        home_menu.add_command(
            label="Dashboard", command=lambda: self.navigate_to(Dashboard.__name__)
        )
        home_menu.add_command(
            label="Studying",
            command=lambda: self.navigate_to("Studying"),
        )
        home_menu.add_command(
            label="Analysis",
            command=lambda: self.navigate_to("Analysis"),
        )

        # Settings menu
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

        if self.profile:
            # Header
            tk.Label(
                container,
                text=f"Welcome {self.profile['username'].split(' ')[0].title()}!",
                font=("Helvatical", 15, "bold"),
                bg=self.backgroundColor,
                fg=PRIMARY_COLOR,
            ).pack(pady=20)

        # Add toggle button for close mode
        toggle_frame = tk.Frame(container, bg=self.backgroundColor)
        toggle_frame.pack(fill=tk.X, pady=5)
        self.close_mode_button = tk.Button(
            toggle_frame,
            text="Manual Close",  # Default mode
            command=self.toggle_close_mode,
            bg=PRIMARY_COLOR,
            fg="white",
        )
        self.close_mode_button.pack(side=tk.LEFT, padx=5)

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

        # Today's Courses Section
        todays_frame = tk.LabelFrame(
            container, text="Today's Courses", bg=self.backgroundColor
        )
        todays_frame.pack(fill=tk.X, pady=10)
        self.show_todays_courses(todays_frame)

        # Materials Section
        materials_frame = tk.LabelFrame(
            container, text="Course Materials", bg=self.backgroundColor
        )
        materials_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.show_materials(materials_frame)

    def toggle_close_mode(self):
        # Toggle the global auto_close flag from App
        self.parent.master.auto_close = not self.parent.master.auto_close
        if self.parent.master.auto_close:
            self.close_mode_button.config(text="Automatic Close")
        else:
            self.close_mode_button.config(text="Manual Close")

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

    def show_todays_courses(self, parent):
        current_day = datetime.now().strftime("%A")
        todays_courses = self.timetable.get(current_day, [])

        if not todays_courses:
            tk.Label(
                parent,
                text="No courses scheduled for today",
                bg=self.backgroundColor,
            ).pack(pady=10)
            return

        for course in todays_courses:
            frame = tk.Frame(parent, bg=self.backgroundColor)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, text=course["name"], bg=self.backgroundColor).pack(
                side=tk.LEFT, padx=5
            )

            course_materials = self.materials_df[
                self.materials_df["course"] == course["name"]
            ]
            if not course_materials.empty:
                material_path = course_materials.iloc[0]["material"]
                tk.Button(
                    frame,
                    text="START STUDY",
                    command=lambda c=course["name"],
                    p=material_path: self.open_material(c, p),
                    bg=PRIMARY_COLOR,
                    fg="white",
                ).pack(side=tk.RIGHT, padx=5)

    def show_materials(self, parent):
        self.study_buttons.clear()  # Clear previous buttons
        for idx, row in self.materials_df.iterrows():
            frame = tk.Frame(parent, bg=self.backgroundColor)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, text=row["course"], bg=self.backgroundColor).pack(
                side=tk.LEFT, padx=5
            )

            # Fix closure issue by creating function factory
            def create_command(course, material, index):
                return lambda: self.open_material(course, material, index)

            study_button = tk.Button(
                frame,
                text="START STUDY",
                command=create_command(row["course"], row["material"], idx),
                bg=PRIMARY_COLOR,
                fg="white",
            )
            study_button.pack(side=tk.RIGHT, padx=5)
            self.study_buttons.append(study_button)

    def navigate_to(self, page_name):
        self.parent.master.show_page(page_name)

    def recordStudyTime(self, course, duration, start, current):
        # Placeholder - implement tracking logic
        pass

    def get_unengaged_courses(self):
        # Placeholder - implement tracking logic
        return []

    def open_material(self, course, material_path, button_idx=None):
        if self.master.master.studying:
            if (
                button_idx is not None
                and self.study_buttons[button_idx]["text"] == "STUDYING..."
            ):
                # Stop the current study session
                self.master.master.stop_study()
                self.study_buttons[button_idx].config(
                    text="START STUDY",
                    command=lambda: self.open_material(
                        course, material_path, button_idx
                    ),
                )
                return
            else:
                messagebox.showerror(
                    "Can't Open Two Materials",
                    "You are already studying! Close the current study to start a new one.",
                )
                return

        if os.path.exists(material_path):
            if os.name == "posix":  # For Linux
                os.system(f'xdg-open "{material_path}"')
            elif os.name == "nt":  # For Windows
                os.system(f'start  .\\"{material_path}"')
            else:
                messagebox.showerror("Error", "Can't open file on this OS!")
                return

            # Update button state if button_idx provided
            if button_idx is not None:
                self.study_buttons[button_idx].config(
                    text="STUDYING...",
                    command=lambda: self.open_material(
                        course, material_path, button_idx
                    ),
                )

            startTime = datetime.now()

            try:
                analytics_df = pd.read_excel("store/analytics.xlsx")
            except FileNotFoundError:
                analytics_df = pd.DataFrame(
                    columns=["course", "duration(s)", "start", "end"]
                )

            today = datetime.now().date()

            if analytics_df.empty:
                existing_duration = 0
                same_day_course = pd.DataFrame()
            else:
                last_start = pd.to_datetime(analytics_df["start"].iloc[-1])
                last_date = last_start.date()
                same_day_course = analytics_df[
                    (analytics_df["course"] == course) & (last_date == today)
                ]
                existing_duration = (
                    int(same_day_course.iloc[-1]["duration(s)"])
                    if not same_day_course.empty
                    else 0
                )

            self.master.master.studying = {
                "course": course,
                "start": startTime,
                "current": startTime,
                "duration": existing_duration,
                "material": material_path,
            }
            self.master.master.startTimer()
        else:
            messagebox.showerror("Error", "Material file not found!")

    def reset_study_buttons(self):
        for idx, row in self.materials_df.iterrows():
            # Fix closure issue by creating function factory
            def create_command(course, material, index):
                return lambda: self.open_material(course, material, index)

            self.study_buttons[idx].config(
                text="START STUDY",
                command=create_command(row["course"], row["material"], idx),
            )
