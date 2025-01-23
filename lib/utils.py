import tkinter as tk


def gap(root: tk.Widget, n: int, direction: str = "y", bg="white") -> tk.Label:
    if direction == "y":
        return tk.Label(root, bg=bg).pack(pady=n)
    else:
        return tk.Label(root).pack(padx=n)
