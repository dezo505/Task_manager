from tkinter import ttk


class TaskInfoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_name_label = ttk.Label(self, text="Nazwa zadania:")
        self.added_date_label = ttk.Label(self, text="Data dodania:")
        self.deadline_label = ttk.Label(self, text="Termin:")
        self.description_label = ttk.Label(self, text="Opis:")
        self.is_done_label = ttk.Label(self, text="Zadanie zakończone:")

        self.task_name_value = ttk.Label(self)
        self.added_date_value = ttk.Label(self)
        self.deadline_value = ttk.Label(self)
        self.description_value = ttk.Label(self)
        self.is_done_value = ttk.Label(self)

        self.task_name_label.grid(row=0, column=0, sticky="w")
        self.added_date_label.grid(row=1, column=0, sticky="w")
        self.deadline_label.grid(row=2, column=0, sticky="w")
        self.description_label.grid(row=3, column=0, sticky="w")
        self.is_done_label.grid(row=4, column=0, sticky="w")

        self.task_name_value.grid(row=0, column=1, sticky="w")
        self.added_date_value.grid(row=1, column=1, sticky="w")
        self.deadline_value.grid(row=2, column=1, sticky="w")
        self.description_value.grid(row=3, column=1, sticky="w")
        self.is_done_value.grid(row=4, column=1, sticky="w")

    def update_task(self, task):
        if task:
            self.task_name_value.config(text=task.name)
            self.added_date_value.config(text=str(task.added_date))
            self.deadline_value.config(text=str(task.deadline))
            self.description_value.config(text=task.description)
            self.is_done_value.config(text="Tak" if task.is_done else "Nie")
        else:
            self.task_name_value.config(text="")
            self.added_date_value.config(text="")
            self.deadline_value.config(text="")
            self.description_value.config(text="")
            self.is_done_value.config(text="")
