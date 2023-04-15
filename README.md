# Aplikacja "Zadaniomat" do zarządzania zadaniami napisana w Phyton 3 przy uzyciu bibliotek SQLite oraz PyQt5

Użytkownik moze tworzyć zadania, przypisywać im kategorie, ustawiać daty wykonania oraz oznaczać zadania jako ukończone.

## Opis techniczny i załozenia projektu:

- aplikacja napisana w języku Python z wykorzystaniem biblioteki PyQt5 do tworzenia interfejsu graficznego,
- aplikacja uzywa SQLite do przechowywania danych o zadaniach,
- aplikacja składa się z trzech klas: Task, TaskManager oraz MainWindow.

## Opis klas:

- Task - klasa reprezentująca pojedyncze zadanie. Powinna zawierać pola takie jak: nazwa zadania, opis, kategoria, data utworzenia, data wykonania oraz informację o tym, czy zadanie zostało ukończone. Klasa powinna mieć możliwość zapisania zadania do bazy danych oraz odczytania z bazy danych,
- TaskManager - klasa odpowiedzialna za zarządzanie zadaniami. Powinna posiadać metody do dodawania nowych zadań, usuwania zadań, oznaczania zadań jako ukończone oraz pobierania listy zadań. Klasa powinna mieć możliwość zapisania stanu listy zadań do bazy danych oraz odczytania z bazy danych,
- MainWindow - klasa reprezentująca główne okno aplikacji. Powinna zawierać pola takie jak: pole tekstowe do wpisywania nazwy zadania, pole tekstowe do wpisywania opisu zadania, pole wyboru kategorii zadania, pole do wpisywania daty wykonania zadania oraz przyciski do dodawania nowego zadania, usuwania zaznaczonego zadania oraz oznaczania zaznaczonego zadania jako ukończone. Klasa powinna mieć możliwość wyświetlenia listy zadań oraz zmiany ich stanu.

## Bibliografia:

- Dokumentacja PyQt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- Dokumentacja SQLite w Pythonie: https://docs.python.org/3/library/sqlite3.html
- Pakiet pysqlite3 implementującej SQLite w Phythonie https://github.com/coleifer/pysqlite3

## Opis klas

Klasa Task zawiera konstruktor, który inicjuje pola klasy oraz metodę save_to_database(), która zapisuje zadanie do bazy danych, oraz metodę get_all_from_database(), która zwraca listę wszystkich zadań z bazy danych.

Klasa TaskManager zawiera konstruktor, który inicjuje pustą listę zadań oraz metody add_task(), remove_task(), mark_task_as_completed() i get_all_tasks(), które odpowiednio dodają nowe zadanie do listy i zapisują je do bazy danych, usuwają zadanie z listy i bazy danych, oznaczają zadanie jako ukończone w liście i bazie danych oraz zwracają listę wszystkich zadań z bazy danych.

Klasa MainWindow tworzy interfejs użytkownika i implementuje logikę aplikacji. Użytkownik może dodawać nowe zadania, usuwać je, oznaczać jako ukończone oraz wyświetlać ich szczegóły. Aplikacja korzysta z klasy TaskManager do zarządzania zadaniami oraz klasy Task do reprezentowania pojedynczych zadań i zapisywania ich do bazy danych.
Plik należy umieścić w tym samym katalogu co plik z kodem aplikacji.

## Wymagania systemowe

- Zainstalowany w systemie Pythona w wersji 3
- Zainstalowany domyślny dla Python3 system zarządzania pakietami o nazwie pip3
- Zainstalowany w systemie SQLite
- Wsparcie dla obsługi biblioteki PyQt5
- Zainstalowane zaleznosci programu np. za pomocą ponizszych komend

```bash
pip3 install PyQt5
pip3 install pysqlite3
```

## Instrukcja instalacji i pierwszego uruchomienia programu

1. Upewnij się, spełniasz wszystkie opsiane powyzej wymagania sprzetowe.
2. Utwórz plik tasks.db z tabelą o następującej strukturze:

```sql
CREATE TABLE tasks (
    created_at TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    category TEXT,
    due_date TEXT,
    completed INTEGER
);
```

1. Uruchom program
   ```python
   python3 -m main.py
   ```
2. Gotowe!

## Rozwiązywanie problemów

W przypadku wystąpienia następującego błędu w tracie instalacją pakietu pysqlite3:

```
ERROR: Failed building wheel for pysqlite3
Running setup.py clean for pysqlite3
Failed to build pysqlite3
ERROR: Could not build wheels for pysqlite3, which is required to install pyproject.toml-based projects
```

nalezy skorzystac z intrukcji opisanej na stronie https://www.pythonpool.com/error-legacy-install-failure/

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

class Task:
def **init**(self, name, description, category, due_date=None, completed=False):
self.name = name
self.description = description
self.category = category
