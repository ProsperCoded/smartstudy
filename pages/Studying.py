import tkinter as tk


class Studying(tk.Tk):
    def __init__(self, parent):
        super.__init__(parent)

    def startTimer(self):
        studying = self.master.studying
        if not studying:
            print("No course is being studied")
            return
        pass

    def stopTimer(self):
        self.master.studying = None
        pass
