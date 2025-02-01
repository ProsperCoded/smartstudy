import tkinter as tk
from lib.theme import PRIMARY_COLOR
from lib.utils import write_to_json, load_from_json
from tkinter import messagebox


class Timetable(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent):
        super().__init__(parent)

        # Days of the week
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Dictionary to store courses for each day
        self.stored_courses = load_from_json("store/timetable.json")
        if not self.stored_courses:
            self.stored_courses = {day: [] for day in self.days}
        self.courses = {day: [] for day in self.days}

        self.create_ui()

    def create_ui(self):
        container = tk.Frame(self)
        container.config(padx=20, pady=20)
        container.pack()

        # Add General Target Hours field
        general_target_frame = tk.Frame(container)
        general_target_frame.grid(row=0, column=0, columnspan=len(self.days), pady=10)

        tk.Label(
            general_target_frame, text="General Target Hours:", font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=5)

        self.general_target = tk.Entry(general_target_frame, width=10)
        self.general_target.pack(side=tk.LEFT, padx=5)
        self.general_target.insert(0, "2")  # Default value

        tk.Button(
            general_target_frame,
            text="Apply to All",
            command=self.apply_general_target,
            bg=PRIMARY_COLOR,
            fg="white",
        ).pack(side=tk.LEFT, padx=5)

        heading = tk.Label(
            container,
            text="SET TIMETABLE",
            font=("Arial", 30, "bold"),
            fg=self.backgroundColor,
        )
        heading.grid(row=1, column=0, columnspan=len(self.days), pady=10)
        # Frame to hold days and their widgets
        self.days_frame = tk.Frame(container)  # Changed from self.parent to self
        self.days_frame.grid(padx=10, pady=10)  # Use grid instead of pack

        for day in self.days:
            # Day label
            day_label = tk.Label(self.days_frame, text=day, font=("Arial", 12, "bold"))
            day_label.grid(row=0, column=self.days.index(day), padx=10, pady=5)

            # Input box for course name
            course_entry = tk.Entry(self.days_frame, width=20)
            course_entry.grid(row=1, column=self.days.index(day), padx=10, pady=5)

            # Add Course button
            add_button = tk.Button(
                self.days_frame,
                text="Add Course",
                command=lambda d=day, e=course_entry: self.add_course(d, e),
            )
            add_button.grid(row=2, column=self.days.index(day), padx=10, pady=5)

            # Frame to display courses for the day
            course_frame = tk.Frame(self.days_frame)
            course_frame.grid(row=3, column=self.days.index(day), padx=10, pady=5)

            # Store the course frame in the dictionary
            self.courses[day].append(course_frame)

            # Prefill the courses if they exist
            if day in self.stored_courses:
                for course in self.stored_courses[day]:
                    # Create a frame for the course and delete button
                    course_item_frame = tk.Frame(course_frame)
                    course_item_frame.pack(fill="x", pady=2)

                    # Add course label
                    course_label = tk.Label(
                        course_item_frame, text=course["name"], font=("Arial", 10)
                    )
                    course_label.pack(side="left")

                    # Add target hours field
                    hours_frame = tk.Frame(course_item_frame)
                    hours_frame.pack(side=tk.LEFT, padx=10)

                    tk.Label(hours_frame, text="hrs:", font=("Arial", 8)).pack(
                        side=tk.LEFT
                    )
                    hours_entry = tk.Entry(hours_frame, width=5)
                    hours_entry.pack(side=tk.LEFT)
                    hours_entry.insert(0, course["target_hours"])
                    hours_entry.bind(
                        "<KeyRelease>", lambda e: self.clear_general_target()
                    )

                    # Add delete button
                    delete_button = tk.Button(
                        course_item_frame,
                        text="✕",
                        command=lambda f=course_item_frame, d=day: self.delete_course(
                            f, d
                        ),
                        font=("Arial", 8),
                        padx=2,
                        pady=0,
                    )
                    delete_button.pack(side="right")

        # Submit button to get all courses
        submit_button = tk.Button(
            self.days_frame,
            text="Submit",
            command=self.store_courses,
            bg=PRIMARY_COLOR,
            fg="white",
        )
        submit_button.grid(row=4, columnspan=len(self.days), pady=10)

    def store_courses(self):
        courses = self.get_courses()
        write_to_json(courses, "store/timetable.json")
        # Refresh main page
        self.parent.master.pages["MainPage"].reload()

    def add_course(self, day, entry):
        course_name = entry.get().strip()
        if not course_name:
            messagebox.showwarning("Input Error", "Please enter a course name.")
            return

        # Add course to the respective day's frame
        course_frame = self.courses[day][0]

        # Create a frame for the course and delete button
        course_item_frame = tk.Frame(course_frame)
        course_item_frame.pack(fill="x", pady=2)

        # Add course label
        course_label = tk.Label(course_item_frame, text=course_name, font=("Arial", 10))
        course_label.pack(side="left")

        # Target hours entry
        hours_frame = tk.Frame(course_item_frame)
        hours_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(hours_frame, text="hrs:", font=("Arial", 8)).pack(side=tk.LEFT)
        hours_entry = tk.Entry(hours_frame, width=5)
        hours_entry.pack(side=tk.LEFT)
        hours_entry.insert(0, self.general_target.get() or "2")
        hours_entry.bind("<KeyRelease>", lambda e: self.clear_general_target())

        # Add delete button
        delete_button = tk.Button(
            course_item_frame,
            text="✕",
            command=lambda: self.delete_course(course_item_frame, day),
            font=("Arial", 8),
            padx=2,
            pady=0,
        )
        delete_button.pack(side="right")

        # Clear the input box
        entry.delete(0, tk.END)

    def delete_course(self, course_frame, day):
        # Remove the course frame
        course_frame.destroy()
        # Update stored courses
        self.store_courses()

    def get_courses(self):
        courses_dict = {}
        for day in self.days:
            courses_dict[day] = [
                {
                    "name": frame.winfo_children()[0].cget("text"),
                    "target_hours": frame.winfo_children()[1].winfo_children()[1].get()
                    or "2",
                }
                for frame in self.courses[day][0].winfo_children()
            ]
        return courses_dict

    def apply_general_target(self):
        target = self.general_target.get()
        if not target.replace(".", "").isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid number")
            return

        for day in self.days:
            for course_frame in self.courses[day][0].winfo_children():
                hours_entry = course_frame.winfo_children()[1].winfo_children()[1]
                hours_entry.delete(0, tk.END)
                hours_entry.insert(0, target)

    def clear_general_target(self):
        self.general_target.delete(0, tk.END)
