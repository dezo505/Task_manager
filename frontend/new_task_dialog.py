import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import DateEntry
from backend.task import Task


class NewTaskDialog(simpledialog.Dialog):
    def __init__(self, parent, task=None):
        self.result = None
        self.task = task
        super().__init__(parent)

    def body(self, parent):
        self.geometry("400x300")
        ttk.Label(parent, text="Name:").grid(row=0, column=0)
        ttk.Label(parent, text="Deadline:").grid(row=1, column=0)
        ttk.Label(parent, text="Description:").grid(row=2, column=0)
        ttk.Label(parent, text="Finished:").grid(row=3, column=0)

        self.name_entry = ttk.Entry(parent)
        self.deadline_entry = DateEntry(parent)
        self.description_text = tk.Text(parent, width=30, height=10)
        self.is_done_var = tk.IntVar()
        self.is_done_checkbutton = ttk.Checkbutton(parent, variable=self.is_done_var)

        self.name_entry.grid(row=0, column=1)
        self.deadline_entry.grid(row=1, column=1)
        self.description_text.grid(row=2, column=1)
        self.is_done_checkbutton.grid(row=3, column=1)

    def buttonbox(self):
        box = ttk.Frame(self)

        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, default="active")
        ok_button.pack(side="left", padx=5, pady=5)

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        task_name = self.name_entry.get()
        deadline = self.deadline_entry.get_date()
        description = self.description_text.get("1.0", tk.END).strip()
        is_done = bool(self.is_done_var.get())

        if not task_name:
            tk.messagebox.showwarning("Error", "Task name can't be blank.")
            return

        task = Task(task_name=task_name, deadline=deadline, description=description, is_done=is_done)
        self.result = task
        super().ok()
