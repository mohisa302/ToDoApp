# infrastructure/sqlite_repo.py
from domain.interfaces import ITodoRepository
import sqlite3
import logging
from domain.interfaces import ITodoRepository
import sqlite3
import logging
from application.models import TodoItem
from typing import List

class SQLiteTodoRepo(ITodoRepository):
    def __init__(self, db_path: str = "todos.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()
        self.logger = logging.getLogger(__name__)

    def _create_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    attachment_filename TEXT,
                    attachment_mimetype TEXT,
                    attachment_data BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Table creation failed: {str(e)}")
            raise

    def add(self, todo: TodoItem) -> TodoItem:
        self.conn.execute(
            "INSERT INTO todos (id, title, completed, attachment_filename, attachment_mimetype, attachment_data) VALUES (?, ?, ?, ?, ?, ?)",
            (todo.id, todo.title, int(todo.completed), todo.attachment_filename, todo.attachment_mimetype, todo.attachment_data)
        )
        self.conn.commit()
        return todo

    def get(self, todo_id: str) -> TodoItem:
        cursor = self.conn.execute(
            "SELECT id, title, completed, attachment_filename, attachment_mimetype, attachment_data FROM todos WHERE id = ?",
            (todo_id,)
        )
        row = cursor.fetchone()
        if row:
            return TodoItem(
                id=row[0],
                title=row[1],
                completed=bool(row[2]),
                attachment_filename=row[3],
                attachment_mimetype=row[4],
                attachment_data=row[5]
            )
        return None

    def update(self, todo: TodoItem) -> TodoItem:
        self.conn.execute(
            "UPDATE todos SET title = ?, completed = ?, attachment_filename = ?, attachment_mimetype = ?, attachment_data = ? WHERE id = ?",
            (todo.title, int(todo.completed), todo.attachment_filename, todo.attachment_mimetype, todo.attachment_data, todo.id)
        )
        self.conn.commit()
        return todo

    def delete(self, todo_id: str) -> None:
        self.conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        self.conn.commit()

    def list_all(self) -> List[TodoItem]:
        cursor = self.conn.execute(
            "SELECT id, title, completed, attachment_filename, attachment_mimetype, attachment_data FROM todos"
        )
        todos = []
        for row in cursor:
            todos.append(TodoItem(
                id=row[0],
                title=row[1],
                completed=bool(row[2]),
                attachment_filename=row[3],
                attachment_mimetype=row[4],
                attachment_data=row[5]
            ))
        return todos
