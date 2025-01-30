import tkinter as tk
from tkinter import filedialog
from lib.theme import PRIMARY_COLOR
from lib.utils import load_from_json
import pandas as pd
import os


class UploadMaterials(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent):
        super().__init__(parent)

        # Track file labels for each course
        self.file_labels = {}
        self.materials_df = None

        # Load courses from timetable
        timetable = load_from_json("store/timetable.json")

        self.all_courses = set()
        for courses in timetable.values():
            self.all_courses.update(map(lambda c: c["name"], courses))

        # Load existing materials
        try:
            self.materials_df = pd.read_excel("store/materials.xlsx")
        except FileNotFoundError:
            self.materials_df = pd.DataFrame(columns=["course", "material"])

        self.create_ui()

    def create_ui(self):
        container = tk.Frame(self)
        container.config(padx=20, pady=20)
        container.pack(expand=True)

        # Headinsg
        tk.Label(
            container,
            text="UPLOAD MATERIALS",
            font=("Arial", 30, "bold"),
            fg=self.backgroundColor,
        ).pack(pady=20)

        # Create frame for courses
        courses_frame = tk.Frame(container)
        courses_frame.pack(pady=20)

        for course in self.all_courses:
            course_frame = tk.Frame(courses_frame)
            course_frame.pack(fill="x", pady=5)

            tk.Label(course_frame, text=course, font=("Arial", 12)).pack(
                side="left", padx=10
            )

            # Create a frame for file info
            file_info_frame = tk.Frame(course_frame)
            file_info_frame.pack(side="left", expand=True, fill="x", padx=10)

            # Create label for file path
            self.file_labels[course] = tk.Label(
                file_info_frame,
                text="",
                font=("Arial", 10),
                wraplength=300,
                justify="left",
            )
            self.file_labels[course].pack(side="left")

            # Add buttons frame
            buttons_frame = tk.Frame(course_frame)
            buttons_frame.pack(side="right")

            # Delete button (hidden initially)
            delete_btn = tk.Button(
                buttons_frame,
                text="✕",
                command=lambda c=course: self.delete_material(c),
                font=("Arial", 8),
                padx=2,
                pady=0,
            )
            self.file_labels[course].delete_btn = delete_btn

            tk.Button(
                buttons_frame,
                text="Upload File",
                command=lambda c=course: self.select_file(c),
                bg=PRIMARY_COLOR,
                fg="white",
            ).pack(side="right", padx=5)

            # Load existing material if any
            existing_material = self.materials_df[self.materials_df["course"] == course]
            if not existing_material.empty:
                path = existing_material.iloc[-1]["material"]
                self.update_file_label(course, path)
        tk.Button(
            courses_frame,
            text="Done",
            # command=lambda c=course: self.select_file(c),
            bg=PRIMARY_COLOR,
            fg="white",
        ).pack(anchor="center", padx=5, pady=10)

    def update_file_label(self, course, file_path):
        if course in self.file_labels:
            self.file_labels[course].config(text=os.path.basename(file_path))
            self.file_labels[course].file_path = file_path
            self.file_labels[course].delete_btn.pack(side="right", padx=5)

    def delete_material(self, course):
        if course in self.file_labels:
            file_path = getattr(self.file_labels[course], "file_path", None)
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

            # Update materials.xlsx
            self.materials_df = self.materials_df[
                self.materials_df["material"] != file_path
            ]
            self.materials_df.to_excel("store/materials.xlsx", index=False)

            # Clear label and hide delete button
            self.file_labels[course].config(text="")
            self.file_labels[course].delete_btn.pack_forget()
            self.file_labels[course].file_path = None

    def select_file(self, course):
        file_path = filedialog.askopenfilename(
            title=f"Select material for {course}",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word files", "*.doc;*.docx"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            # Create materials directory if it doesn't exist
            materials_dir = "store/materials"
            course_dir = os.path.join(materials_dir, course)
            os.makedirs(course_dir, exist_ok=True)

            # Copy file to materials directory
            filename = os.path.basename(file_path)
            destination = os.path.join(course_dir, filename)

            with open(file_path, "rb") as src, open(destination, "wb") as dst:
                dst.write(src.read())

            self.update_file_label(course, destination)
            self.record_material(course, destination)

    def record_material(self, course, destination):
        # Remove any existing record for this course
        self.materials_df = self.materials_df[self.materials_df["course"] != course]

        # Add new record
        new_record = pd.DataFrame({"course": [course], "material": [destination]})
        self.materials_df = pd.concat(
            [self.materials_df, new_record], ignore_index=True
        )
        self.materials_df.to_excel("store/materials.xlsx", index=False)
