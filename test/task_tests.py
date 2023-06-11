import unittest
from datetime import datetime, timedelta

from backend.task import Task


class TestTask(unittest.TestCase):

    def test_create_task(self):
        task = Task(task_id=1, task_name="Test task", added_date=datetime.now().date(),
                    deadline=datetime.now().date() + timedelta(days=5),
                    description="This is a test task", is_done=False)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.name, "Test task")
        self.assertEqual(task.added_date, datetime.now().date())
        self.assertEqual(task.deadline, datetime.now().date() + timedelta(days=5))
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.is_done, False)

    def test_str_representation(self):
        task = Task(task_id=1, task_name="Test task", added_date=datetime.now().date(),
                    deadline=datetime.now().date() + timedelta(days=5),
                    description="This is a test task", is_done=False)

        expected_str = f"Task: Test task\nAdded date: {datetime.now().date()}\nDeadline: {datetime.now().date() + timedelta(days=5)}\nDescription: This is a test task\nIs Done: False"
        self.assertEqual(str(task), expected_str)


if __name__ == '__main__':
    unittest.main()
