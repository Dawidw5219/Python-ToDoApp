import os
import sqlite3


def __init__():
    if os.path.exists("zadania.db"):
        os.remove("zadania.db")
    polacznie = sqlite3.connect('zadania.db')
    c = polacznie.cursor()
    sql_komenda = """
        CREATE TABLE zadania (
            utworzono TEXT PRIMARY KEY,
            nazwa TEXT,
            opis TEXT,
            kategoria TEXT,
            termin TEXT,
            ukonczono INTEGER
        );
        """
    c.execute(sql_komenda)
    print("Baza danych w pliku zadania.db zostala utworzona")


if __name__ == "__main__":
    __init__()
