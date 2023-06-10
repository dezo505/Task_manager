import tkinter as tk
from tkinter import ttk

from backend.task_journal import TaskJournal
from frontend.edit_task_dialog import EditTaskDialog
from frontend.new_task_dialog import NewTaskDialog
from frontend.task_info_frame import TaskInfoFrame


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task manager")
        self.geometry("800x600")

        self.task_journal = TaskJournal()
        self.create_widgets()

        self.selected_task = None

        self.task_map = {}
        self.update_task_map()
        self.refresh_task_treeview()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = ttk.Frame(self)
        self.right_frame = ttk.Frame(self)

        self.add_task_button = ttk.Button(self, text="Dodaj zadanie", command=self.show_new_task_dialog)

        self.task_treeview = ttk.Treeview(self.left_frame, selectmode="browse", show="tree")
        self.task_treeview.bind('<<TreeviewSelect>>', self.handle_task_selection)

        self.task_info_frame = TaskInfoFrame(self.right_frame)
        self.task_info_frame.grid(row=0, column=0, sticky="nswe")

        self.edit_task_button = ttk.Button(self.right_frame, text="Edytuj zadanie", command=self.show_edit_task_dialog)

        self.delete_task_button = ttk.Button(self.right_frame, text="Usuń zadanie", command=self.delete_task)

        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.right_frame.grid(row=0, column=1, sticky="nswe")
        self.add_task_button.grid(row=1, column=0, columnspan=2)
        self.task_treeview.grid(sticky="nswe")
        self.edit_task_button.grid(row=1, column=0, sticky="nswe")
        self.delete_task_button.grid(row=1, column=1, sticky="nswe")

        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)

    def show_new_task_dialog(self):
        dialog = NewTaskDialog(self)
        if dialog.result is not None:
            task = dialog.result
            self.task_journal.add_task(task)
            self.update_task_map()
            self.refresh_task_treeview()

    def show_edit_task_dialog(self):
        dialog = EditTaskDialog(self, task=self.selected_task)
        if dialog.result is not None:
            self.task_journal.edit_task(
                self.selected_task.id,
                name=dialog.result.name,
                deadline=dialog.result.deadline,
                description=dialog.result.description,
                is_done=dialog.result.is_done
            )
            self.update_task_map()
            self.refresh_task_treeview()
            self.refresh_task_info_frame()

    def delete_task(self):
        if self.selected_task:
            self.task_journal.delete_task(self.selected_task.id)
            self.update_task_map()
            self.refresh_task_treeview()
            self.refresh_task_info_frame()

    def update_task_map(self):
        tasks = self.task_journal.get_all_tasks()
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
            tasks_for_date = [task.name for task in self.task_map[date]]
            date_item = self.task_treeview.insert('', tk.END, str(date), text=str(date), open=True)
            for task_name in tasks_for_date:
                self.task_treeview.insert(date_item, tk.END, text=task_name)

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



if __name__ == "__main__":
    app = Application()
    app.mainloop()
