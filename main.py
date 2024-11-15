import json
from datetime import datetime


class Task:
    def __init__(self, id, title, description, status="новая", priority="средний"):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            data["id"],
            data["title"],
            data["description"],
            data["status"],
            data["priority"]
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        return task


class TaskManager:
    status_options = ["новая", "в работе", "завершена"]
    priority_options = ["низкий", "средний", "высокий"]

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def add_task(self, title, description, priority="средний"):
        priority = self.validate_input(priority, self.priority_options, "средний")
        task = Task(self.next_id, title, description, priority=priority)
        self.tasks.append(task)
        self.next_id += 1

    def edit_task(self, task_id, title=None, description=None, status=None, priority=None):
        task = next((t for t in self.tasks if t.id == int(task_id)), None)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if status:
                task.status = self.validate_input(status, self.status_options, task.status)
            if priority:
                task.priority = self.validate_input(priority, self.priority_options, task.priority)

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != int(task_id)]

    def list_tasks(self, status_filter=None, priority_filter=None):
        filtered_tasks = self.tasks
        if status_filter:
            filtered_tasks = [t for t in filtered_tasks if t.status == status_filter]
        if priority_filter:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority_filter]
        return sorted(filtered_tasks, key=lambda t: t.created_at)

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
                self.tasks = [Task.from_dict(data) for data in tasks_data]
                self.next_id = max(int(task.id) for task in self.tasks) + 1 if self.tasks else 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            self.next_id = 1

    def display_options(self, options):
        return ", ".join(options)

    def validate_input(self, value, options, default):
        if value.lower() in options:
            return value.lower()
        else:
            print(f"Неверное значение! Установлено значение по умолчанию '{default}'.")
            return default


def main():
    manager = TaskManager()

    while True:
        print("\nМенеджер задач:")
        print("1. Создать задачу")
        print("2. Редактировать задачу")
        print("3. Удалить задачу")
        print("4. Просмотр задач")
        print("5. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            print(f"Доступные приоритеты: {manager.display_options(TaskManager.priority_options)}")
            priority = input("Выберите приоритет (по умолчанию 'средний'): ").lower() or "средний"
            manager.add_task(title, description, priority)
            print("Задача добавлена.")

        elif choice == "2":
            task_id = input("Введите ID задачи: ")
            title = input("Новое название (нажмите Enter, чтобы пропустить): ")
            description = input("Новое описание (нажмите Enter, чтобы пропустить): ")
            print(f"Доступные статусы: {manager.display_options(TaskManager.status_options)}")
            status = input("Выберите статус (новая, в работе, завершена): ").lower()
            print(f"Доступные приоритеты: {manager.display_options(TaskManager.priority_options)}")
            priority = input("Выберите приоритет (нажмите Enter, чтобы пропустить): ").lower()
            manager.edit_task(task_id, title, description, status, priority)
            print("Задача обновлена.")

        elif choice == "3":
            task_id = input("Введите ID задачи для удаления: ")
            manager.delete_task(task_id)
            print("Задача удалена.")

        elif choice == "4":
            print(f"Доступные статусы для фильтрации: {manager.display_options(TaskManager.status_options)}")
            status = input("Фильтр по статусу (нажмите Enter, чтобы пропустить): ").lower()
            print(f"Доступные приоритеты для фильтрации: {manager.display_options(TaskManager.priority_options)}")
            priority = input("Фильтр по приоритету (нажмите Enter, чтобы пропустить): ").lower()
            tasks = manager.list_tasks(
                status_filter=status if status in TaskManager.status_options else None,
                priority_filter=priority if priority in TaskManager.priority_options else None
            )
            for task in tasks:
                formatted_time = task.created_at.strftime("%H:%M")
                print(
                    f"{task.id} | {task.title} | {task.description} | {task.status} | {task.priority} | {formatted_time}")

        elif choice == "5":
            manager.save_tasks()
            print("Задачи сохранены. До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()