import tkinter as tk
from tkinter import simpledialog

from tkcalendar import DateEntry

from backend.task import Task


class EditTaskDialog(simpledialog.Dialog):
    def __init__(self, parent, task):
        self.result = None
        self.task = task
        super().__init__(parent)

    def body(self, parent):
        self.geometry("400x300")
        tk.Label(parent, text="Nazwa zadania:").grid(row=0, column=0)
        tk.Label(parent, text="Deadline:").grid(row=1, column=0)
        tk.Label(parent, text="Opis:").grid(row=2, column=0)
        tk.Label(parent, text="Czy wykonane:").grid(row=3, column=0)

        self.name_entry = tk.Entry(parent)
        self.deadline_entry = DateEntry(parent)
        self.description_text = tk.Text(parent, width=30, height=10)
        self.is_done_var = tk.IntVar()
        self.is_done_checkbutton = tk.Checkbutton(parent, variable=self.is_done_var)

        self.name_entry.grid(row=0, column=1)
        self.deadline_entry.grid(row=1, column=1)
        self.description_text.grid(row=2, column=1)
        self.is_done_checkbutton.grid(row=3, column=1)

        self.name_entry.insert(tk.END, self.task.name)
        self.deadline_entry.set_date(self.task.deadline)
        self.description_text.insert(tk.END, self.task.description)
        self.is_done_var.set(int(self.task.is_done))

    def ok(self, event=None):
        task_name = self.name_entry.get()
        deadline = self.deadline_entry.get_date()
        description = self.description_text.get("1.0", tk.END).strip()
        is_done = bool(self.is_done_var.get())
        task = Task(task_id=self.task.id, task_name=task_name, deadline=deadline, description=description, is_done=is_done)
        self.result = task
        super().ok()
