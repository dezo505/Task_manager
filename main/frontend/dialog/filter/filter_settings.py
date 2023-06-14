class FilterSettings:
    def __init__(self, show_done_tasks=True, show_not_done_tasks=True, max_deadline_days=7, max_deadline_days_past=3):
        self.show_done_tasks = show_done_tasks
        self.show_not_done_tasks = show_not_done_tasks
        self.max_deadline_days = max_deadline_days
        self.max_deadline_days_past = max_deadline_days_past
