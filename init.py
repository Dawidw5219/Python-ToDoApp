import sqlite3
polacznie = sqlite3.connect('zadania.db')
c = polacznie.cursor()
sql_create_projects_table = """
CREATE TABLE zadania (
    utworzono TEXT PRIMARY KEY,
    nazwa TEXT,
    opis TEXT,
    kategoria TEXT,
    termin TEXT,
    ukonczono INTEGER
);
"""
c.execute(sql_create_projects_table)
