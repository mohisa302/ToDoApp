"""
This module provides an in-memory implementation of the TodoRepository
for managing Todo items.
"""

from infrastructure.repositories import TodoRepository
from application.models import TodoItem

class InMemoryTodoRepo(TodoRepository):
    """
    InMemoryTodoRepo is a class that implements the TodoRepository interface
    for managing Todo items in memory.
    """

    def __init__(self):
        """Initialize the in-memory repository."""
        self.todos = {}

    def add(self, todo: TodoItem):
        """
        Add a new Todo item to the repository.
        
        :param todo: The Todo item to be added.
        :return: The added Todo item.
        """
        self.todos[todo.id] = todo
        return todo

    def get(self, todo_id: str) -> TodoItem:
        """
        Get a Todo item by its ID.
        
        :param todo_id: The ID of the Todo item.
        :return: The Todo item with the specified ID.
        """
        return self.todos.get(todo_id)

    def update(self, todo: TodoItem):
        """
        Update an existing Todo item in the repository.
        
        :param todo: The Todo item to be updated.
        :return: The updated Todo item.
        :raises ValueError: If the Todo item is not found.
        """
        if todo.id not in self.todos:
            raise ValueError("Todo not found")
        self.todos[todo.id] = todo
        return todo

    def delete(self, todo_id: str):
        """
        Delete a Todo item from the repository by its ID.
        
        :param todo_id: The ID of the Todo item to be deleted.
        """
        if todo_id in self.todos:
            del self.todos[todo_id]

    def list_all(self):
        """
        List all Todo items in the repository.
        
        :return: A list of all Todo items.
        """
        return list(self.todos.values())
