import sqlite3
from datetime import datetime


class Zadanie:
    def __init__(self, name, description, category, due_date=None, completed=False):
        self.created_at = datetime.now()
        self.name = name
        self.description = description
        self.category = category
        self.due_date = due_date
        self.completed = completed

    def save_to_database(self):
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (name, description, category, created_at, due_date, completed) VALUES (?, ?, ?, ?, ?, ?)',
                  (self.name, self.description, self.category, self.created_at, self.due_date, self.completed))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_from_database():
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tasks')
        rows = c.fetchall()
        tasks = []
        for row in rows:
            task = Zadanie(row[1], row[2], row[3], row[4], row[5])
            task.created_at = datetime.fromisoformat(row[0])
            # task.completed = bool(row[5])
            tasks.append(task)
        conn.close()
        return tasks
