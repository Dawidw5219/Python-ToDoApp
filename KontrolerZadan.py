import sqlite3
from Zadanie import Zadanie

###
# Klasa KontrolerZadan zawiera konstruktor, który inicjuje pustą listę zadań oraz metody dodaj_zadanie(), usun_zadanie(), oznacz_jako_ukonczone() i wszystkie_zadania(), które odpowiednio dodają nowe zadanie do listy i zapisują je do bazy danych, usuwają zadanie z listy i bazy danych, oznaczają zadanie jako ukończone w liście i bazie danych oraz zwracają listę wszystkich zadań z bazy danych.
###


class KontrolerZadan:
    def __init__(self):
        self.zadania = []

    def dodaj_zadanie(self, task):
        task.zapisz_do_bazy()
        self.zadania.append(task)

    def usun_zadanie(self, index):
        zadanie = self.zadania[index]
        polacznie = sqlite3.connect('zadania.db')
        c = polacznie.cursor()
        c.execute('DELETE FROM zadania WHERE utworzono = ?',
                  (zadanie.utworzono.isoformat(),))
        polacznie.commit()
        polacznie.close()
        self.zadania.pop(index)

    def oznacz_jako_ukonczone(self, index):
        zadanie = self.zadania[index]
        zadanie.completed = True
        polacznie = sqlite3.connect('zadania.db')
        xdd = "%r" % (zadanie.utworzono.isoformat())
        c = polacznie.cursor()
        komenda = 'UPDATE zadania SET ukonczono = 1 WHERE utworzono = ' + xdd
        # '"
        c.execute(komenda)
        polacznie.commit()
        polacznie.close()
        self.wszystkie_zadania()
        print(xdd)
        print(komenda)

    def wszystkie_zadania(self):
        self.zadania = Zadanie.odczytaj_wszystkie_z_bazy()
        return self.zadania
