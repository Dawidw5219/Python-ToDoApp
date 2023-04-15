import sqlite3
from datetime import datetime

###
# Klasa Zadania zawiera konstruktor, który inicjuje pola klasy oraz metodę zapisz_do_bazy(), która zapisuje zadanie do bazy danych, oraz metodę odczytaj_wszystkie_z_bazy(), która zwraca listę wszystkich zadań z bazy danych.
###
class Zadanie:
    def __init__(self, nazwa, opis, kategoria, termin=None, ukonczono=False):
        self.datetime = datetime.now()
        self.utworzono = self.datetime.isoformat()
        self.nazwa = nazwa
        self.opis = opis
        self.kategoria = kategoria
        self.termin = termin
        self.ukonczono = ukonczono

    def zapisz_do_bazy(self):
        polacznie = sqlite3.connect('zadania.db')
        c = polacznie.cursor()
        c.execute('INSERT INTO zadania (nazwa, opis, kategoria, utworzono, termin, ukonczono) VALUES (?, ?, ?, ?, ?, ?)',
                  (self.nazwa, self.opis, self.kategoria, self.utworzono, self.termin, self.ukonczono))
        polacznie.commit()
        polacznie.close()

    @staticmethod
    def odczytaj_wszystkie_z_bazy():
        polacznie = sqlite3.connect('zadania.db')
        c = polacznie.cursor()
        c.execute('SELECT * FROM zadania')
        wiersze = c.fetchall()
        print(wiersze)
        zadania = []
        for wiersz in wiersze:
            zadanie = Zadanie(wiersz[1], wiersz[2],
                              wiersz[3], wiersz[4], wiersz[5])
            zadanie.utworzono = datetime.fromisoformat(wiersz[0])
            # task.completed = bool(row[5])
            zadania.append(zadanie)
        polacznie.close()
        return zadania
