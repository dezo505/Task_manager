import tkinter as tk
from datetime import datetime
from tkinter import ttk
from ttkthemes import ThemedTk

from backend.task_journal import TaskJournal
from frontend.dialog.edit_task_dialog import EditTaskDialog
from frontend.dialog.filter.filter_dialog import FilterDialog
from frontend.dialog.filter.filter_settings import FilterSettings
from frontend.dialog.new_task_dialog import NewTaskDialog
from frontend.frame.task_info_frame import TaskInfoFrame


class Application(ThemedTk):
    def __init__(self, theme="arc", *args, **kwargs):
        super().__init__(theme=theme, *args, **kwargs)
        self.title("Task manager")
        self.geometry("750x500")
        self.resizable(False, False)

        self.task_journal = TaskJournal()
        self.create_widgets()

        self.selected_task = None
        self.filter_settings = FilterSettings()

        self.task_map = {}
        self.update_task_map()
        self.refresh_task_treeview()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=1, minsize=300)

        self.left_frame = ttk.Frame(self)
        self.right_frame = ttk.Frame(self)

        self.add_task_button = ttk.Button(self, text="Add task", command=self.show_new_task_dialog, width=20)

        self.treeview_frame = ttk.Frame(self.left_frame)

        self.task_treeview = ttk.Treeview(self.treeview_frame, selectmode="browse", show="tree")
        self.task_treeview.bind('<<TreeviewSelect>>', self.handle_task_selection)

        self.v_scrollbar = ttk.Scrollbar(self.treeview_frame, orient='vertical', command=self.task_treeview.yview)
        self.h_scrollbar = ttk.Scrollbar(self.treeview_frame, orient='horizontal', command=self.task_treeview.xview)

        self.task_treeview.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.task_treeview.tag_configure("finished", foreground="gray", font=("Helvetica", 10))
        self.task_treeview.tag_configure("in_progress", foreground="black", font=("Helvetica", 10, "bold"))

        self.task_info_frame = TaskInfoFrame(self.right_frame)
        self.task_info_frame.grid(row=0, column=0, sticky="nswe")

        self.edit_task_button = ttk.Button(self.right_frame, text="Edit task", command=self.show_edit_task_dialog, width=20)

        self.delete_task_button = ttk.Button(self.right_frame, text="Delete task", command=self.delete_task, width=20)

        self.filter_button = ttk.Button(self, text="Filter", command=self.show_filter_dialog, width=20)

        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.right_frame.grid(row=0, column=1, sticky="nswe")
        self.add_task_button.grid(row=1, column=0, columnspan=2)
        self.task_treeview.grid(row=0, column=0, sticky="nswe")
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.treeview_frame.grid(sticky="nswe")
        self.edit_task_button.grid(row=1, column=0)
        self.delete_task_button.grid(row=2, column=0)
        self.filter_button.grid(row=2, column=0, columnspan=2)

        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 5))
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=(5, 0))

    def show_new_task_dialog(self):
        self.treeview_frame.grid_propagate(False)
        dialog = NewTaskDialog(self)
        if dialog.result is not None:
            task = dialog.result
            result = self.task_journal.add_task(task)
            if not result:
                tk.messagebox.showwarning("Error", "Something went wrong, task wasn't added.")
                return
            self.selected_task = task
            self.update_task_map()
            self.refresh_task_treeview()

    def show_edit_task_dialog(self):
        self.treeview_frame.grid_propagate(False)
        if not self.selected_task:
            tk.messagebox.showwarning("Error", "No task was selected.")
            return

        dialog = EditTaskDialog(self, task=self.selected_task)
        if dialog.result is not None:
            result = self.task_journal.edit_task(
                self.selected_task.id,
                name=dialog.result.name,
                deadline=dialog.result.deadline,
                description=dialog.result.description,
                is_done=dialog.result.is_done
            )
            if not result:
                tk.messagebox.showwarning("Error", "Something went wrong, task wasn't edited.")
                return

            self.update_task_map()
            self.refresh_task_treeview()
            self.refresh_task_info_frame()

    def show_filter_dialog(self):
        self.treeview_frame.grid_propagate(False)
        FilterDialog(self, self.filter_settings)
        self.selected_task = None
        self.update_task_map()
        self.refresh_task_treeview()
        self.refresh_task_info_frame()

    def delete_task(self):
        if not self.selected_task:
            tk.messagebox.showwarning("Error", "No task was selected.")
            return

        result = self.task_journal.delete_task(self.selected_task.id)

        if not result:
            tk.messagebox.showwarning("Error", "Something went wrong, task wasn't deleted.")
            return

        self.update_task_map()
        self.refresh_task_treeview()
        self.refresh_task_info_frame()

    def update_task_map(self):
        tasks = self.task_journal.get_all_tasks()
        today = datetime.today().date()

        if not self.filter_settings.show_done_tasks:
            tasks = list(filter(lambda x: x.is_done is not True, tasks))

        if not self.filter_settings.show_not_done_tasks:
            tasks = list(filter(lambda x: x.is_done is not False, tasks))

        if self.filter_settings.max_deadline_days is not None:
            tasks = list(
                filter(
                    lambda x: x.deadline is None or (x.deadline - today).days <= self.filter_settings.max_deadline_days,
                    tasks))

        if self.filter_settings.max_deadline_days_past is not None:
            tasks = list(
                filter(lambda x: x.deadline is None or (
                            today - x.deadline).days <= self.filter_settings.max_deadline_days_past,
                       tasks))

        self.task_map.clear()
        for task in tasks:
            if task.deadline in self.task_map:
                self.task_map[task.deadline].append(task)
            else:
                self.task_map[task.deadline] = [task]

    def refresh_task_treeview(self):
        for item in self.task_treeview.get_children():
            self.task_treeview.delete(item)

        sorted_dates = sorted(self.task_map.keys(), key=lambda x: (x is None, x))

        for date in sorted_dates:
            tasks_for_date = self.task_map[date]  # Przyjmijmy, że to jest lista obiektów zadania
            date_item = self.task_treeview.insert('', tk.END, str(date), text=str(date), open=True)
            for task in tasks_for_date:
                tag = 'finished' if task.is_done else 'in_progress'  # Zakładamy, że task ma atrybut lub metodę is_finished
                self.task_treeview.insert(date_item, tk.END, text=task.name, tags=(tag,))

    def refresh_task_info_frame(self):
        self.task_info_frame.update_task(self.selected_task)

    def handle_task_selection(self, event):
        selected_item = self.task_treeview.focus()
        selected_item_parent = self.task_treeview.parent(selected_item)

        if selected_item_parent:
            task_date = self.task_treeview.item(selected_item_parent)['text']
            task_name = self.task_treeview.item(selected_item)['text']

            self.selected_task = self.task_journal.get_task_by_name_and_deadline(task_name, task_date)
            self.refresh_task_info_frame()
