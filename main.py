from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime
import Task


class Task:
    def __init__(self, name, description, category, due_date=None, completed=False):
        self.name = name
        self.description = description
        self.category = category


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle
