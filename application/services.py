import os
import mimetypes
from application.models import TodoItem
from domain.interfaces import ITodoRepository

class TodoService:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def create_todo(self, title: str, attachment_data: bytes = None, **kwargs):
        if len(title) > 100:
            raise ValueError("Title too long")
        return self.repository.add(TodoItem(title=title, **kwargs))
    
    def add_todo(
        self,
        title: str,
        attachment_path: str = None,
        attachment_data: bytes = None,
        attachment_filename: str = None,
        attachment_mimetype: str = None
    ) -> TodoItem:
        if attachment_path and not attachment_data:
            if os.path.getsize(attachment_path) > 5 * 1024 * 1024:
                raise ValueError("File too large. Maximum allowed size is 5MB.")
            attachment_filename = os.path.basename(attachment_path)
            attachment_mimetype, _ = mimetypes.guess_type(attachment_path)
            with open(attachment_path, "rb") as f:
                attachment_data = f.read()
        if attachment_data and len(attachment_data) > 5 * 1024 * 1024:
            raise ValueError("File too large. Maximum allowed size is 5MB.")
        todo = TodoItem(
            title=title,
            attachment_filename=attachment_filename,
            attachment_mimetype=attachment_mimetype,
            attachment_data=attachment_data
        )
        self.repository.add(todo)
        return todo

    def update_todo(
        self,
        todo_id: str,
        title: str = None,
        attachment_path: str = None,
        attachment_data: bytes = None,
        attachment_filename: str = None,
        attachment_mimetype: str = None,
        completed: bool = None
    ):
        todo = self.repository.get(todo_id)
        if not todo:
            raise ValueError("Todo not found")
        if title is not None:
            todo.title = title
        if attachment_path or attachment_data:
            if attachment_path and not attachment_data:
                if os.path.getsize(attachment_path) > 5 * 1024 * 1024:
                    raise ValueError("File too large. Maximum allowed size is 5MB.")
                attachment_filename = os.path.basename(attachment_path)
                attachment_mimetype, _ = mimetypes.guess_type(attachment_path)
                with open(attachment_path, "rb") as f:
                    attachment_data = f.read()
            if attachment_data and len(attachment_data) > 5 * 1024 * 1024:
                raise ValueError("File too large. Maximum allowed size is 5MB.")
            todo.attachment_filename = attachment_filename
            todo.attachment_mimetype = attachment_mimetype
            todo.attachment_data = attachment_data
        if completed is not None:
            todo.completed = completed
        self.repository.update(todo)
        return todo

    def delete_todo(self, todo_id: str):
        self.repository.delete(todo_id)

    def list_todos(self):
        return self.repository.list_all()
