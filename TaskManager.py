import sqlite3
from Task import Zadanie


class KontrolerZadan:
    def __init__(self):
        self.tasks = []

    def init_table(self):
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        sql_create_projects_table = """
        CREATE TABLE tasks (
            created_at TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT,
            due_date TEXT,
            completed INTEGER
        );
        """
        c.execute(sql_create_projects_table)

    def add_task(self, task):
        task.save_to_database()
        self.tasks.append(task)

    def remove_task(self, index):
        task = self.tasks[index]
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE created_at = ?',
                  (task.created_at.isoformat(),))
        conn.commit()
        conn.close()
        self.tasks.pop(index)

    def mark_task_as_completed(self, index):
        task = self.tasks[index]
        task.completed = True
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('UPDATE tasks SET completed = ? WHERE created_at = ?',
                  (True, task.created_at.isoformat()))
        conn.commit()
        conn.close()

    def get_all_tasks(self):
        self.tasks = Zadanie.get_all_from_database()
        return self.tasks
