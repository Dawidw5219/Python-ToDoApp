import sqlite3


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
