import json
import tkinter as tk


def gap(root: tk.Widget, n: int, direction: str = "y", bg="white") -> tk.Label:
    if direction == "y":
        return tk.Label(root, bg=bg).pack(pady=n)
    else:
        return tk.Label(root).pack(padx=n)


def write_to_json(data, filename):
    """
    Write data to a JSON file.

    :param data: Python dictionary (or any serializable object) to write to the file.
    :param filename: Name of the JSON file (e.g., "data.json").
    """
    try:
        with open(filename, "w") as file:
            json.dump(
                data, file, indent=4
            )  # Use indent for pretty-printing(not important)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")


def load_from_json(filename):
    """
    Load data from a JSON file.

    :param filename: Name of the JSON file (e.g., "data.json").
    :return: Python dictionary (or the data structure stored in the file).
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"Data successfully loaded from {filename}")
        return data
    except FileNotFoundError:
        print(f"File {filename} not found. Creating a new one.")
        return {}  # * if file doesn't exists return an empty dictionary
    except Exception as e:
        print(f"Error loading from {filename}: {e}")
        return None
