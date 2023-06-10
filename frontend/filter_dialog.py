import tkinter as tk
from tkinter import simpledialog, IntVar, BooleanVar

class FilterDialog(simpledialog.Dialog):
    def __init__(self, parent, filter_settings):
        self.filter_settings = filter_settings
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="Pokaż zadania zrobione:").grid(row=0, sticky='w')
        tk.Label(master, text="Pokaż zadania niezrobione:").grid(row=1, sticky='w')
        tk.Label(master, text="Pokaż zadania z terminem do X dni:").grid(row=2, sticky='w')
        tk.Label(master, text="Pokaż zadania, które minęły co najwyżej X dni temu:").grid(row=3, sticky='w')

        self.done_var = BooleanVar(value=self.filter_settings.show_done_tasks)
        self.not_done_var = BooleanVar(value=self.filter_settings.show_not_done_tasks)
        self.max_deadline_days_var = IntVar(value=self.filter_settings.max_deadline_days)
        self.max_deadline_days_past = IntVar(value=self.filter_settings.max_deadline_days_past)

        tk.Checkbutton(master, variable=self.done_var).grid(row=0, column=1, sticky='w')
        tk.Checkbutton(master, variable=self.not_done_var).grid(row=1, column=1, sticky='w')
        tk.Entry(master, textvariable=self.max_deadline_days_var).grid(row=2, column=1, sticky='w')
        tk.Entry(master, textvariable=self.max_deadline_days_past).grid(row=3, column=1, sticky='w')

    def apply(self):
        self.filter_settings.show_done_tasks = self.done_var.get()
        self.filter_settings.show_not_done_tasks = self.not_done_var.get()
        self.filter_settings.max_deadline_days = self.max_deadline_days_var.get()
        self.filter_settings.max_deadline_days_past = self.max_deadline_days_past.get()
