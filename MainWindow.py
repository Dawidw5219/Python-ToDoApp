import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime
from TaskManager import KontrolerZadan
from Task import Zadanie


class Interfejs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aplikacja ToDo: Zadaniomat')
        self.task_manager = KontrolerZadan()
        self.inicjalizacja_ui()

    def inicjalizacja_ui(self):
        # create widgets
        name_label = QLabel('Nazwa:')
        self.name_input = QLineEdit()
        description_label = QLabel('Opis:')
        self.description_input = QTextEdit()
        category_label = QLabel('Kategoria:')
        self.category_input = QComboBox()
        self.category_input.addItems(['Praca', 'Prywatne', 'Inne'])
        due_date_label = QLabel('Termin (koniecznie w formacie YYYY-MM-DD): ')
        self.due_date_input = QLineEdit()
        add_button = QPushButton('Dodaj zadanie')
        remove_button = QPushButton('Usuń zadanie')
        mark_as_completed_button = QPushButton('Oznacz jako ukończone')
        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.SingleSelection)

        # layout
        form_layout = QGridLayout()
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(description_label, 1, 0)
        form_layout.addWidget(self.description_input, 1, 1)
        form_layout.addWidget(category_label, 2, 0)
        form_layout.addWidget(self.category_input, 2, 1)
        form_layout.addWidget(due_date_label, 3, 0)
        form_layout.addWidget(self.due_date_input, 3, 1)
        form_layout.addWidget(add_button, 4, 0, 1, 2)
        form_layout.addWidget(remove_button, 5, 0, 1, 2)
        form_layout.addWidget(mark_as_completed_button, 6, 0, 1, 2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.task_list)

        # widzety
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # przyciski
        add_button.clicked.connect(self.dodaj_zadanie)
        remove_button.clicked.connect(self.usun_zadanie)
        mark_as_completed_button.clicked.connect(self.odznacz_zadanie)
        self.task_list.itemDoubleClicked.connect(self.pokaz_szczegoly)

        # zaladowanie danych z sqla
        self.zaladuj_zadania()

    def zaladuj_zadania(self):
        self.task_list.clear()
        tasks = self.task_manager.get_all_tasks()
        for task in tasks:
            item = QListWidgetItem(task.name)
            if task.completed:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)
            self.task_list.addItem(item)

    def dodaj_zadanie(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        category = self.category_input.currentText()
        due_date = self.due_date_input.text()
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        task = Zadanie(name, description, category, due_date)
        self.task_manager.add_task(task)
        self.zaladuj_zadania()
        self.wyczysc_formularz()

    def usun_zadanie(self):
        index = self.task_list.currentRow()
        if index >= 0:
            confirm = QMessageBox.question(
                self, 'Zatwierdz', 'Jestes pewny, ze chcesz usunac to zadanie?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.task_manager.remove_task(index)
                self.zaladuj_zadania()

    def odznacz_zadanie(self):
        index = self.task_list.currentRow()
        if index >= 0:
            self.task_manager.mark_task_as_completed(index)
            self.zaladuj_zadania()

    def pokaz_szczegoly(self, item):
        index = self.task_list.currentRow()
        task = self.task_manager.tasks[index]
        message = f'Nazwa: {task.name}\nOpis: {task.description}\nKategoria: {task.category}\nUworzono: {task.created_at}\nTermin: {task.due_date}\nWykonano: {task.completed}'
        QMessageBox.information(self, 'Szczegóły zadania', message)

    def wyczysc_formularz(self):
        self.name_input.clear()
        self.description_input.clear()
        self.category_input.setCurrentIndex(0)
        self.due_date_input.clear()


app = QApplication(sys.argv)
window = Interfejs()
window.show()
sys.exit(app.exec_())
