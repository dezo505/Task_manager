import sqlite3
import datetime
import logging
from backend.task import Task

logging.basicConfig(level=logging.INFO)


class TaskJournal:
    def __init__(self, db_name='task_journal.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            added_date TEXT NOT NULL,
            deadline TEXT,
            description TEXT,
            is_done INTEGER NOT NULL,
            UNIQUE (task_name, deadline)
        )
        """)
        self.connection.commit()

    def add_task(self, task):
        logging.info(f"Adding task to journal:\n{task}")
        self.cursor.execute("""
        INSERT INTO tasks (task_name, added_date, deadline, description, is_done)
        VALUES (?, ?, ?, ?, ?)
        """, (task.name, task.added_date.strftime('%Y-%m-%d'),
              task.deadline.strftime('%Y-%m-%d') if task.deadline else None, task.description, int(task.is_done)))
        self.connection.commit()

    def row_to_task(self, row):
        return Task(row[0], row[1], datetime.datetime.strptime(row[2], '%Y-%m-%d').date(),
                    datetime.datetime.strptime(row[3], '%Y-%m-%d').date() if row[3] else None,
                    row[4], bool(row[5]))

    def get_all_tasks(self):
        self.cursor.execute("""
        SELECT * FROM tasks
        """)
        return [self.row_to_task(row) for row in self.cursor.fetchall()]

    def get_tasks_due_in_days(self, days):
        date_limit = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        self.cursor.execute("""
        SELECT * FROM tasks WHERE deadline <= ? AND is_done = 0
        """, (date_limit,))
        return [self.row_to_task(row) for row in self.cursor.fetchall()]

    def get_tasks_due_this_week(self):
        return self.get_tasks_due_in_days(7)

    def get_undone_tasks(self):
        self.cursor.execute("""
        SELECT * FROM tasks WHERE is_done = 0
        """)
        return [self.row_to_task(row) for row in self.cursor.fetchall()]

    def edit_task(self, task_id, task_name=None, added_date=None, deadline=None, description=None, is_done=None):
        if not any([task_name, added_date, deadline, description, is_done is not None]):
            logging.error("At least one task property must be provided for the update.")
            return

        query = "UPDATE tasks SET "
        params = []

        if task_name:
            query += "task_name = ?, "
            params.append(task_name)
        if added_date:
            query += "added_date = ?, "
            params.append(added_date.strftime('%Y-%m-%d'))
        if deadline:
            query += "deadline = ?, "
            params.append(deadline.strftime('%Y-%m-%d'))
        if description:
            query += "description = ?, "
            params.append(description)
        if is_done is not None:
            query += "is_done = ?, "
            params.append(int(is_done))

        query = query[:-2] + " WHERE id = ?"
        params.append(task_id)

        self.cursor.execute(query, tuple(params))
        self.connection.commit()

    def delete_task(self, task_id):
        logging.info(f"Deleting task with id {task_id} from journal.")
        self.cursor.execute("""
        DELETE FROM tasks WHERE id = ?
        """, (task_id,))
        self.connection.commit()

    def get_task_by_name_and_deadline(self, name, deadline):
        self.cursor.execute("""
                SELECT * FROM tasks
                WHERE task_name = ? AND deadline = ?
                """, (name, deadline))

        row = self.cursor.fetchone()

        if row is not None:
            return Task(task_id=row[0], task_name=row[1], added_date=row[2], deadline=row[3], description=row[4], is_done=row[5])
        else:
            return None

    def __del__(self):
        self.connection.close()
