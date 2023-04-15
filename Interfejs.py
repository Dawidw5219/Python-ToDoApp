import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime
from KontrolerZadan import KontrolerZadan
from Zadanie import Zadanie

###
# Klasa Interfejs tworzy interfejs użytkownika i implementuje logikę aplikacji. Użytkownik może dodawać nowe zadania, usuwać je, oznaczać jako ukończone oraz wyświetlać ich szczegóły. Aplikacja korzysta z klasy KontrolerZadan do zarządzania zadaniami oraz klasy Zadanie do reprezentowania pojedynczych zadań i zapisywania ich do bazy danych.
###


class Interfejs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aplikacja ToDo: Zadaniomat')
        self.kontroler_zadan = KontrolerZadan()
        self.inicjalizacja_ui()

    def inicjalizacja_ui(self):
        nazwa_etykieta = QLabel('Nazwa:')
        self.nazwa_etykieta = QLineEdit()
        opis_etykieta = QLabel('Opis:')
        self.opis_etykieta = QTextEdit()
        category_label = QLabel('Kategoria:')
        self.kategorie = QComboBox()
        self.kategorie.addItems(['Praca', 'Prywatne', 'Inne'])
        due_date_label = QLabel('Termin (koniecznie w formacie YYYY-MM-DD): ')
        self.termin_pole = QLineEdit()
        dodaj_etykieta = QPushButton('Dodaj zadanie')
        usun_etykieta = QPushButton('Usuń zadanie')
        oznacz_jako_ukoncone_etykieta = QPushButton('Oznacz jako ukończone')
        kliknij_po_szczegoly = QLabel(
            'Kliknij dwuktortnie w dowolne zadanie z listy, aby wyświelić szczegóły')
        self.lista_zadan = QListWidget()
        self.lista_zadan.setSelectionMode(QListWidget.SingleSelection)

        formularz = QGridLayout()
        formularz.addWidget(nazwa_etykieta, 0, 0)
        formularz.addWidget(self.nazwa_etykieta, 0, 1)
        formularz.addWidget(opis_etykieta, 1, 0)
        formularz.addWidget(self.opis_etykieta, 1, 1)
        formularz.addWidget(category_label, 2, 0)
        formularz.addWidget(self.kategorie, 2, 1)
        formularz.addWidget(due_date_label, 3, 0)
        formularz.addWidget(self.termin_pole, 3, 1)
        formularz.addWidget(dodaj_etykieta, 4, 0, 1, 2)
        formularz.addWidget(usun_etykieta, 5, 0, 1, 2)
        formularz.addWidget(oznacz_jako_ukoncone_etykieta, 6, 0, 1, 2)
        formularz.addWidget(kliknij_po_szczegoly, 7, 0, 1, 2)

        interfejs_glowny = QVBoxLayout()
        interfejs_glowny.addLayout(formularz)
        interfejs_glowny.addWidget(self.lista_zadan)

        widget = QWidget()
        widget.setLayout(interfejs_glowny)
        self.setCentralWidget(widget)

        dodaj_etykieta.clicked.connect(self.dodaj_zadanie)
        usun_etykieta.clicked.connect(self.usun_zadanie)
        oznacz_jako_ukoncone_etykieta.clicked.connect(
            self.odznacz_zadanie)
        self.lista_zadan.itemDoubleClicked.connect(self.pokaz_szczegoly)

        self.zaladuj_zadania()

    def zaladuj_zadania(self):
        self.lista_zadan.clear()
        zadania = self.kontroler_zadan.wszystkie_zadania()
        for zadanie in zadania:
            element = QListWidgetItem(zadanie.nazwa)
            if zadanie.ukonczono:
                element.setFlags(element.flags() | Qt.ItemIsUserCheckable)
                element.setCheckState(Qt.Checked)
            self.lista_zadan.addItem(element)

    def dodaj_zadanie(self):
        nazwa = self.nazwa_etykieta.text()
        opis = self.opis_etykieta.toPlainText()
        kategoria = self.kategorie.currentText()
        termin = self.termin_pole.text()
        if termin:
            termin = datetime.strptime(termin, '%Y-%m-%d')
        zadanie = Zadanie(nazwa, opis, kategoria, termin)
        self.kontroler_zadan.dodaj_zadanie(zadanie)
        self.zaladuj_zadania()
        self.wyczysc_formularz()

    def usun_zadanie(self):
        i = self.lista_zadan.currentRow()
        if i >= 0:
            potwierdz = QMessageBox.question(
                self, 'Zatwierdz', 'Jestes pewny, ze chcesz usunac to zadanie?', QMessageBox.Yes | QMessageBox.No)
            if potwierdz == QMessageBox.Yes:
                self.kontroler_zadan.usun_zadanie(i)
                self.zaladuj_zadania()

    def odznacz_zadanie(self):
        i = self.lista_zadan.currentRow()
        if i >= 0:
            self.kontroler_zadan.oznacz_jako_ukonczone(i)
            self.zaladuj_zadania()

    def pokaz_szczegoly(self, item):
        i = self.lista_zadan.currentRow()
        zadanie = self.kontroler_zadan.zadania[i]
        wiadomosc = f'Nazwa: {zadanie.nazwa}\nOpis: {zadanie.opis}\nKategoria: {zadanie.kategoria}\nUworzono: {zadanie.utworzono}\nTermin: {zadanie.termin}\nWykonano: {zadanie.ukonczono}'
        QMessageBox.information(self, 'Szczegóły zadania', wiadomosc)

    def wyczysc_formularz(self):
        self.nazwa_etykieta.clear()
        self.opis_etykieta.clear()
        self.kategorie.setCurrentIndex(0)
        self.termin_pole.clear()


app = QApplication(sys.argv)
window = Interfejs()
window.show()
sys.exit(app.exec_())
