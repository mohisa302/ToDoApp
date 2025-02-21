from abc import ABC, abstractmethod
from typing import List
from application.models import TodoItem
class ITodoRepository(ABC):
    @abstractmethod
    def add(self, todo: TodoItem) -> TodoItem:
        pass

    @abstractmethod
    def get(self, todo_id: str) -> TodoItem:
        pass

    @abstractmethod
    def update(self, todo: TodoItem) -> TodoItem:
        pass

    @abstractmethod
    def delete(self, todo_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[TodoItem]:
        pass
