import json
from pathlib import Path
from infrastructure.repositories import TodoRepository
from application.models import TodoItem

class FileTodoRepo(TodoRepository):
    def __init__(self, file_path: str = "todos.json"):
        self.file_path = Path(file_path)
        self.todos = {}
        self._load()

    def _load(self):
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.todos = {todo["id"]: TodoItem(**todo) for todo in data}

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump([todo.__dict__ for todo in self.todos.values()], f, indent=4)

    def add(self, todo: TodoItem):
        self.todos[todo.id] = todo
        self._save()
        return todo

    def get(self, todo_id: str) -> TodoItem:
        return self.todos.get(todo_id)

    def update(self, todo: TodoItem):
        if todo.id not in self.todos:
            raise ValueError("Todo not found")
        self.todos[todo.id] = todo
        self._save()
        return todo

    def delete(self, todo_id: str):
        if todo_id in self.todos:
            del self.todos[todo_id]
            self._save()

    def list_all(self):
        return list(self.todos.values())
