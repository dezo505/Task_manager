from tkinter import ttk, Text, Scrollbar, N, S, E, W, END


class TaskInfoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_name_label = ttk.Label(self, text="Name:")
        self.added_date_label = ttk.Label(self, text="Added date:")
        self.deadline_label = ttk.Label(self, text="Deadline:")
        self.description_label = ttk.Label(self, text="Description:")
        self.is_done_label = ttk.Label(self, text="Finished:")

        self.task_name_value = ttk.Label(self)
        self.added_date_value = ttk.Label(self)
        self.deadline_value = ttk.Label(self)
        self.description_value = Text(self, height=4, wrap='word', state='disabled')
        self.is_done_value = ttk.Label(self)

        self.description_scrollbar = Scrollbar(self, command=self.description_value.yview)
        self.description_value['yscrollcommand'] = self.description_scrollbar.set

        self.task_name_label.grid(row=0, column=0, sticky="w")
        self.added_date_label.grid(row=1, column=0, sticky="w")
        self.deadline_label.grid(row=2, column=0, sticky="w")
        self.description_label.grid(row=3, column=0, sticky="w")
        self.is_done_label.grid(row=4, column=0, sticky="w")

        self.task_name_value.grid(row=0, column=1, sticky="w")
        self.added_date_value.grid(row=1, column=1, sticky="w")
        self.deadline_value.grid(row=2, column=1, sticky="w")
        self.description_value.grid(row=3, column=1, sticky=W + E)
        self.description_scrollbar.grid(row=3, column=2, sticky=N + S)
        self.is_done_value.grid(row=4, column=1, sticky="w")

    def update_task(self, task):
        self.description_value.config(state="normal")
        if task:
            self.task_name_value.config(text=task.name)
            self.added_date_value.config(text=str(task.added_date))
            self.deadline_value.config(text=str(task.deadline))

            self.description_value.delete("1.0", END)
            self.description_value.insert("1.0", task.description)

            self.is_done_value.config(text="Tak" if task.is_done else "Nie")
        else:
            self.task_name_value.config(text="")
            self.added_date_value.config(text="")
            self.deadline_value.config(text="")
            self.description_value.delete("1.0", END)
            self.is_done_value.config(text="")
        self.description_value.config(state="disabled")
