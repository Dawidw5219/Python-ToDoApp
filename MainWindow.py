from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime
import TaskManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task Manager')
        self.task_manager = TaskManager()
        self.init_ui()

    def init_ui(self):
        # create widgets
        name_label = QLabel('Name:')
        self.name_input = QLineEdit()
        description_label = QLabel('Description:')
        self.description_input = QTextEdit()
        category_label = QLabel('Category:')
        self.category_input = QComboBox()
        self.category_input.addItems(['Work', 'Personal', 'Other'])
        due_date_label = QLabel('Due date:')
        self.due_date_input = QLineEdit()
        add_button = QPushButton('Add')
        remove_button = QPushButton('Remove')
        mark_as_completed_button = QPushButton('Mark as completed')
        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.SingleSelection)

        # create layout
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

        # create widget
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # connect signals and slots
        add_button.clicked.connect(self.add_task)
        remove_button.clicked.connect(self.remove_task)
        mark_as_completed_button.clicked.connect(self.mark_task_as_completed)
        self.task_list.itemDoubleClicked.connect(self.show_task_details)

        # load tasks from database
        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        tasks = self.task_manager.get_all_tasks()
        for task in tasks:
            item = QListWidgetItem(task.name)
            if task.completed:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)
            self.task_list.addItem(item)

    def add_task(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        category = self.category_input.currentText()
        due_date = self.due_date_input.text()
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        task = Task(name, description, category, due_date)
        self.task_manager.add_task(task)
        self.load_tasks()
        self.clear_form()

    def remove_task(self):
        index = self.task_list.currentRow()
        if index >= 0:
            confirm = QMessageBox.question(
                self, 'Confirm', 'Are you sure you want to remove this task?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.task_manager.remove_task(index)
                self.load_tasks()

    def mark_task_as_completed(self):
        index = self.task_list.currentRow()
        if index >= 0:
            self.task_manager.mark_task_as_completed(index)
            self.load_tasks()

    def show_task_details(self, item):
        index = self.task_list.currentRow()
        task = self.task_manager.tasks[index]
        message = f'Name: {task.name}\nDescription: {task.description}\nCategory: {task.category}\nCreated at: {task.created_at}\nDue date: {task.due_date}\nCompleted: {task.completed}'
        QMessageBox.information(self, 'Task details', message)

    def clear_form(self):
        self.name_input.clear()
        self.description_input.clear()
        self.category_input.setCurrentIndex(0)
        self.due_date_input.clear()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
