from tkinter import ttk, simpledialog, IntVar, BooleanVar


class FilterDialog(simpledialog.Dialog):
    def __init__(self, parent, filter_settings):
        self.filter_settings = filter_settings
        super().__init__(parent)

    def body(self, master):
        ttk.Label(master, text="Show finished tasks:").grid(row=0, sticky='w')
        ttk.Label(master, text="Show not finished tasks:").grid(row=1, sticky='w')
        ttk.Label(master, text="Show tasks with a deadline within X days:").grid(row=2, sticky='w')
        ttk.Label(master, text="Show tasks that were due at most X days ago:").grid(row=3, sticky='w')

        self.done_var = BooleanVar(value=self.filter_settings.show_done_tasks)
        self.not_done_var = BooleanVar(value=self.filter_settings.show_not_done_tasks)
        self.max_deadline_days_var = IntVar(value=self.filter_settings.max_deadline_days)
        self.max_deadline_days_past = IntVar(value=self.filter_settings.max_deadline_days_past)

        ttk.Checkbutton(master, variable=self.done_var).grid(row=0, column=1, sticky='w')
        ttk.Checkbutton(master, variable=self.not_done_var).grid(row=1, column=1, sticky='w')
        ttk.Entry(master, textvariable=self.max_deadline_days_var).grid(row=2, column=1, sticky='w')
        ttk.Entry(master, textvariable=self.max_deadline_days_past).grid(row=3, column=1, sticky='w')

    def buttonbox(self):
        box = ttk.Frame(self)

        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, default="active")
        ok_button.pack(side="left", padx=5, pady=5)

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        self.filter_settings.show_done_tasks = self.done_var.get()
        self.filter_settings.show_not_done_tasks = self.not_done_var.get()
        self.filter_settings.max_deadline_days = self.max_deadline_days_var.get()
        self.filter_settings.max_deadline_days_past = self.max_deadline_days_past.get()
