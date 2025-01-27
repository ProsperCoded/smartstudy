import tkinter as tk
from lib.utils import write_to_json
from lib.utils import load_from_json
from tkinter import messagebox


class Timetable(tk.Frame):
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
        print("stored_courses", self.stored_courses)
        if not self.stored_courses:
            self.stored_courses = {day: [] for day in self.days}
        self.courses = {day: [] for day in self.days}

        self.create_ui()

    def create_ui(self):
        # Frame to hold days and their respective widgets
        self.days_frame = tk.Frame(self)  # Changed from self.parent to self
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
                        course_item_frame, text=course, font=("Arial", 10)
                    )
                    course_label.pack(side="left")

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
            self.days_frame, text="Submit", command=self.store_courses
        )
        submit_button.grid(row=4, columnspan=len(self.days), pady=10)

    def store_courses(self):
        courses = self.get_courses()
        write_to_json(courses, "store/timetable.json")

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
                frame.winfo_children()[0].cget(
                    "text"
                )  # Get text from label (first child)
                for frame in self.courses[day][0].winfo_children()
            ]
        return courses_dict
