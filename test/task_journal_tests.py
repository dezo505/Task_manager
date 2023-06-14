import unittest
from unittest.mock import MagicMock
from datetime import datetime
from main.main import Task
from main.main import TaskJournal, row_to_task


class TestTaskJournal(unittest.TestCase):

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.task_journal = TaskJournal(db_name="test.db")
        self.task_journal.connection = self.mock_conn
        self.task_journal.cursor = self.mock_cursor

    def test_row_to_task(self):
        mock_row = (1, "Test task", "2023-06-10", "2023-06-15", "This is a test task", 0)
        task = row_to_task(mock_row)

        self.assertEqual(task.id, mock_row[0])
        self.assertEqual(task.name, mock_row[1])
        self.assertEqual(task.added_date, datetime.strptime(mock_row[2], '%Y-%m-%d').date())
        self.assertEqual(task.deadline, datetime.strptime(mock_row[3], '%Y-%m-%d').date() if mock_row[3] else None)
        self.assertEqual(task.description, mock_row[4])
        self.assertEqual(task.is_done, bool(mock_row[5]))

    def test_add_task(self):
        task = Task(task_id=1, task_name="Test task", added_date=datetime.now().date(),
                    deadline=datetime.now().date(), description="This is a test task", is_done=False)

        self.task_journal.task_with_name_and_deadline_exists = MagicMock(return_value=False)
        self.assertTrue(self.task_journal.add_task(task))
        self.mock_cursor.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_add_task_exists(self):
        task = Task(task_id=1, task_name="Test task", added_date=datetime.now().date(),
                    deadline=datetime.now().date(), description="This is a test task", is_done=False)

        self.task_journal.task_with_name_and_deadline_exists = MagicMock(return_value=True)
        self.assertFalse(self.task_journal.add_task(task))
        self.mock_cursor.execute.assert_not_called()
        self.mock_conn.commit.assert_not_called()

    def test_get_all_tasks(self):
        mock_rows = [
            (1, "Test task", "2023-06-10", "2023-06-15", "This is a test task", False),
            (2, "Another task", "2023-06-11", "2023-06-16", "This is another task", True),
        ]
        self.mock_cursor.fetchall.return_value = mock_rows

        tasks = self.task_journal.get_all_tasks()

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, mock_rows[0][0])
        self.assertEqual(tasks[0].name, mock_rows[0][1])
        self.assertEqual(tasks[1].id, mock_rows[1][0])
        self.assertEqual(tasks[1].name, mock_rows[1][1])

    def test_edit_task(self):
        task_id = 1
        name = "Updated task"
        self.task_journal.task_with_id_exists = MagicMock(return_value=True)
        self.task_journal.get_task_by_name_and_deadline = MagicMock(return_value=None)

        self.assertTrue(self.task_journal.edit_task(task_id, name=name))
        self.mock_cursor.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_delete_task(self):
        task_id = 1
        self.task_journal.task_with_id_exists = MagicMock(return_value=True)

        self.assertTrue(self.task_journal.delete_task(task_id))
        self.mock_cursor.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_delete_task_not_exists(self):
        task_id = 1
        self.task_journal.task_with_id_exists = MagicMock(return_value=False)

        self.assertFalse(self.task_journal.delete_task(task_id))
        self.mock_cursor.execute.assert_not_called()
        self.mock_conn.commit.assert_not_called()

    def test_get_task_by_name_and_deadline(self):
        name = "Test task"
        deadline = "2023-06-15"
        mock_row = (1, "Test task", "2023-06-10", "2023-06-15", "This is a test task", False)
        self.mock_cursor.fetchone.return_value = mock_row

        task = self.task_journal.get_task_by_name_and_deadline(name, deadline)

        self.assertEqual(task.id, mock_row[0])
        self.assertEqual(task.name, mock_row[1])

    def test_task_with_name_and_deadline_exists(self):
        name = "Test task"
        deadline = datetime.now().date()
        self.mock_cursor.fetchone.return_value = [1]

        self.assertTrue(self.task_journal.task_with_name_and_deadline_exists(name, deadline))

    def test_task_with_name_and_deadline_not_exists(self):
        name = "Test task"
        deadline = datetime.now().date()
        self.mock_cursor.fetchone.return_value = None

        self.assertFalse(self.task_journal.task_with_name_and_deadline_exists(name, deadline))

    def test_task_with_id_exists(self):
        task_id = 1
        self.mock_cursor.fetchone.return_value = [1]

        self.assertTrue(self.task_journal.task_with_id_exists(task_id))

    def test_task_with_id_not_exists(self):
        task_id = 1
        self.mock_cursor.fetchone.return_value = None

        self.assertFalse(self.task_journal.task_with_id_exists(task_id))

    def tearDown(self):
        self.task_journal.connection.close()


if __name__ == '__main__':
    unittest.main()
