import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
from lib.theme import PRIMARY_COLOR


class Analysis(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_ui()

    def create_ui(self):
        container = tk.Frame(self, bg=self.backgroundColor)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        tk.Label(
            container,
            text="WEEKLY STUDY ANALYSIS",
            font=("Arial", 24, "bold"),
            bg=self.backgroundColor,
        ).pack(pady=20)

        # Frame for the graph
        self.graph_frame = tk.Frame(container, bg=self.backgroundColor)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.update_graph()

    def update_graph(self):
        try:
            # Clear existing graph
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            # Load and process data
            df = pd.read_excel("store/analytics.xlsx")
            if df.empty:
                self.show_no_data_message()
                return

            # Convert timestamps to datetime
            df["start"] = pd.to_datetime(df["start"])
            df["end"] = pd.to_datetime(df["end"])

            # Calculate start of week (Monday)
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())
            week_start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
            week_end = week_start + timedelta(days=7)

            # Filter for current week
            mask = (df["start"] >= week_start) & (df["start"] < week_end)
            week_df = df[mask].copy()

            if week_df.empty:
                self.show_no_data_message()
                return

            # Add day name column
            week_df["day"] = week_df["start"].dt.strftime("%A")

            # Aggregate duration by day and course
            grouped = (
                week_df.groupby(["day", "course"])["duration(s)"].sum().reset_index()
            )
            # Convert seconds to hours
            grouped["hours"] = grouped["duration(s)"] / 3600

            # Create the visualization
            fig = Figure(figsize=(12, 6))
            ax = fig.add_subplot(111)

            days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            courses = grouped["course"].unique()
            bar_width = 0.8 / len(courses)

            for i, course in enumerate(courses):
                course_data = grouped[grouped["course"] == course]
                x = range(len(days))
                y = []
                for day in days:
                    hours = course_data[course_data["day"] == day]["hours"].sum()
                    y.append(hours)

                ax.bar(
                    [xi + i * bar_width for xi in x], y, width=bar_width, label=course
                )

            ax.set_ylabel("Hours")
            ax.set_title("Study Hours by Course and Day")
            ax.set_xticks(range(len(days)))
            ax.set_xticklabels(days, rotation=45)
            ax.legend()

            # Embed the graph in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except FileNotFoundError:
            self.show_no_data_message()
        except Exception as e:
            print(f"Error creating graph: {e}")
            self.show_error_message()

    def show_no_data_message(self):
        tk.Label(
            self.graph_frame,
            text="No study data available for this week",
            font=("Arial", 14),
            bg=self.backgroundColor,
            fg=PRIMARY_COLOR,
        ).pack(expand=True)

    def show_error_message(self):
        tk.Label(
            self.graph_frame,
            text="Error loading analytics data",
            font=("Arial", 14),
            bg=self.backgroundColor,
            fg="red",
        ).pack(expand=True)
