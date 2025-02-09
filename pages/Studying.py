import tkinter as tk
from datetime import timedelta
import pandas as pd
import os
import time
from threading import Thread
from lib.theme import PRIMARY_COLOR
import subprocess


class Studying(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.timer_running = False
        self.timer_id = None
        self.create_ui()

    def create_ui(self):
        container = tk.Frame(self, bg="white")
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Message for non-studying state
        self.non_studying_message = tk.Label(
            container,
            text="Not currently studying. Go to the main page and click on a course to study.",
            font=("Arial", 14),
            bg="white",
            fg=PRIMARY_COLOR,
            wraplength=400,
        )

        # Course Info Section
        info_frame = tk.Frame(container, bg="white")
        info_frame.pack(pady=20)

        self.course_label = tk.Label(
            info_frame, text="", font=("Arial", 24, "bold"), bg="white"
        )
        self.course_label.pack()

        self.material_label = tk.Label(
            info_frame, text="", font=("Arial", 12), bg="white"
        )
        self.material_label.pack()

        # Timer Display
        timer_frame = tk.Frame(container, bg="white")
        timer_frame.pack(expand=True)

        self.timer_label = tk.Label(
            timer_frame,
            text="00:00:00",
            font=("Arial", 48, "bold"),
            bg="white",
            fg=PRIMARY_COLOR,
        )
        self.timer_label.pack(pady=40)

        # Controls
        control_frame = tk.Frame(container, bg="white")
        control_frame.pack(pady=20)

        self.stop_button = tk.Button(
            control_frame,
            text="STOP TIMER",
            command=self.stop_timer,
            bg=PRIMARY_COLOR,
            fg="white",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10,
        )
        self.stop_button.pack(side=tk.RIGHT, padx=5)

    def update_study_info(self):
        studying = self.parent.master.studying
        print("updating study info,", studying)
        if studying:
            self.non_studying_message.pack_forget()
            self.course_label.config(text=studying["course"])
            self.material_label.config(text=os.path.basename(studying["material"]))
            # Reset elements incase they have been closed
            self.course_label.pack()
            self.material_label.pack()
            self.stop_button.pack()
            self.timer_label.pack(pady=40)
            self.start_timer()
        else:
            # Hide timer elements
            self.course_label.pack_forget()
            self.material_label.pack_forget()
            self.timer_label.pack_forget()
            self.stop_button.pack_forget()
            # Show non-studying message
            self.non_studying_message.pack(expand=True)

    def start_timer(self):
        self.timer_running = True
        # Create a separate thread for the timer
        self.timer_thread = Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

    def check_file_open(self, file_path):
        if os.name == "nt":
            # ! This doesn't work curretnly because of some WINDOWS limitations
            try:
                with open(file_path, "rb+"):
                    return False
            except Exception:
                return True
        else:
            try:
                output = subprocess.check_output(
                    ["lsof", file_path], stderr=subprocess.DEVNULL
                )
                return True
            except subprocess.CalledProcessError:
                return False

    def run_timer(self):
        while self.timer_running:
            studying = self.parent.master.studying
            if (
                studying
                and self.master.master.auto_close
                and not self.check_file_open(studying["material"])
            ):
                print("Material file was closed, stopping timer...")
                self.stop_timer()
                return
            self.update_timer()
            time.sleep(1)

    def update_timer(self):
        if not self.timer_running:
            return

        studying = self.parent.master.studying
        if not studying:
            return
        print("timer is running")
        duration = studying["duration"] = studying["duration"] + 1
        startTime = studying["start"]

        # Use timedelta to properly add seconds
        studying["current"] = startTime + timedelta(seconds=duration)

        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60

        self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # Update analytics every second
        self.update_analytics(studying)

    def stop_timer(self):
        self.timer_running = False
        studying = self.parent.master.studying
        if studying:
            self.save_final_analytics(studying)
            self.parent.master.studying = None

        # Refresh relevant pages
        main_page = self.parent.master.pages["Dashboard"]
        analysis_page = self.parent.master.pages["Analysis"]
        main_page.reload()
        analysis_page.reload()

        self.update_study_info()
        self.parent.master.show_page("Dashboard")

    def update_analytics(self, studying):
        try:
            # Load existing analytics or create new DataFrame
            try:
                df = pd.read_excel("store/analytics.xlsx")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["course", "duration(s)", "start", "end"])

            # Update current session data
            current_session = {
                "course": studying["course"],
                "duration(s)": studying["duration"],
                "start": studying["start"],
                "end": studying["current"],
            }

            # Instead of always checking only the last entry, find any record that matches same day & course:
            same_day_course_df = df[
                (df["course"] == studying["course"])
                & (pd.to_datetime(df["start"]).dt.date == studying["start"].date())
            ]
            if not same_day_course_df.empty:
                # Update existing entry
                index_to_update = same_day_course_df.index[-1]
                df.at[index_to_update, "duration(s)"] = studying["duration"]
                df.at[index_to_update, "end"] = studying["current"]
            else:
                # Append current session
                df = pd.concat([df, pd.DataFrame([current_session])], ignore_index=True)

            # Save updated analytics
            df.to_excel("store/analytics.xlsx", index=False)
        except Exception as e:
            print(f"Error updating analytics: {e}")

    def save_final_analytics(self, studying):
        try:
            df = pd.read_excel("store/analytics.xlsx")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["course", "duration(s)", "start", "end"])

        # Use the same day/course check as above; update if exists, otherwise create
        same_day_course_df = df[
            (df["course"] == studying["course"])
            & (pd.to_datetime(df["start"]).dt.date == studying["start"].date())
        ]

        if not same_day_course_df.empty:
            index_to_update = same_day_course_df.index[-1]
            df.at[index_to_update, "duration(s)"] = studying["duration"]
            df.at[index_to_update, "end"] = studying["current"]
        else:
            # Record final session data
            final_session = {
                "course": studying["course"],
                "duration(s)": studying["duration"],
                "start": studying["start"],
                "end": studying["current"],
            }
            df = pd.concat([df, pd.DataFrame([final_session])], ignore_index=True)

        df.to_excel("store/analytics.xlsx", index=False)
