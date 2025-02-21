"""
This module defines the abstract base class for the TodoRepository
which outlines the methods required for managing Todo items.
"""

from abc import ABC, abstractmethod
from typing import List
from application.models import TodoItem

class TodoRepository(ABC):
    """
    TodoRepository is an abstract base class that defines the methods
    required for managing Todo items.
    """

    @abstractmethod
    def add(self, todo: TodoItem):
        """
        Add a new Todo item to the repository.
        
        :param todo: The Todo item to be added.
        """
        pass

    @abstractmethod
    def get(self, todo_id: str) -> TodoItem:
        """
        Get a Todo item by its ID.
        
        :param todo_id: The ID of the Todo item.
        :return: The Todo item with the specified ID.
        """
        pass

    @abstractmethod
    def update(self, todo: TodoItem):
        """
        Update an existing Todo item in the repository.
        
        :param todo: The Todo item to be updated.
        """
        pass

    @abstractmethod
    def delete(self, todo_id: str):
        """
        Delete a Todo item from the repository by its ID.
        
        :param todo_id: The ID of the Todo item to be deleted.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[TodoItem]:
        """
        List all Todo items in the repository.
        
        :return: A list of all Todo items.
        """
        pass
