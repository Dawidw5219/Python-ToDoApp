import sqlite3
import Task


class TaskManager:
    def __init__(self):
        self.tasks = []

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
        self.tasks = Task.get_all_from_database()
        return self.tasks
