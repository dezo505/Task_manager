from datetime import datetime


class Task:
    def __init__(self, task_id=None, task_name=None, added_date=datetime.now().date(), deadline=None, description=None, is_done=False):
        self.id = task_id
        self.name = task_name
        self.added_date = added_date
        self.deadline = deadline
        self.description = description
        self.is_done = is_done

    def __str__(self):
        return f"Task: {self.name}\nAdded date: {self.added_date}\nDeadline: {self.deadline}\nDescription: {self.description}\nIs Done: {self.is_done}"
