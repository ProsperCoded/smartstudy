import tkinter as tk
import lib.utils as utils
from lib.theme import PRIMARY_COLOR


class Profile:
    username: str
    firstName: str
    lastName: str

    def __init__(self, username: str, age: int, firstName, lastName):
        self.username = username


class ProfileWindow(tk.Frame):
    backgroundColor = "white"

    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        container = tk.Frame(self)
        container.config(bg=self.backgroundColor, padx=20, pady=20)
        # ? Place at the center
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add widgets to container
        tk.Label(
            container,
            text="PLEASE ENTER YOUR BIO",
            bg=self.backgroundColor,
            font=("Arial", 20, "bold"),
        ).pack(padx=20)
        utils.gap(container, 10)

        # widget specific frame
        widgetFrame = tk.Frame(container, bg=self.backgroundColor)
        widgetFrame.pack()
        tk.Label(widgetFrame, text="USER NAME", bg=self.backgroundColor).pack(
            anchor=tk.W
        )
        self.userNameEntry = tk.Entry(widgetFrame, width=30, bg=self.backgroundColor)
        self.userNameEntry.pack()

        utils.gap(widgetFrame, 10)
        tk.Label(widgetFrame, text="EMAIL", bg=self.backgroundColor).pack(anchor=tk.W)
        self.emailEntry = tk.Entry(widgetFrame, width=30, bg=self.backgroundColor)
        self.emailEntry.pack()

        self.pack(fill=tk.BOTH, expand=True)

        submitButton = tk.Button(
            container, text="SUBMIT", bg=PRIMARY_COLOR, fg="white", command=self.submit
        )
        submitButton.pack(pady=10)

    def submit(self):
        username = self.userNameEntry.get()
        email = self.emailEntry.get()
        userProfile = {"username": username, "email": email}
        storeFileName = "store/UserProfile.json"
        print(userProfile)
        utils.write_to_json(userProfile, storeFileName)
        pass
