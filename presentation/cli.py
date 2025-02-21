"""
This module provides a command-line interface (CLI) for managing Todo items
using different storage backends (in-memory, file, SQLite).
"""

import click
from application.services import TodoService
from infrastructure.in_memory_repo import InMemoryTodoRepo
from infrastructure.file_repo import FileTodoRepo
from infrastructure.sqlite_repo import SQLiteTodoRepo

@click.group()
@click.option('--storage', default='memory', help='Storage type [memory|file|sqlite]')
@click.pass_context
def cli(ctx, storage):
    """
    CLI entry point for managing Todo items.
    
    :param storage: The storage type to be used [memory|file|sqlite].
    """
    if storage == "memory":
        repo = InMemoryTodoRepo()
    elif storage == "file":
        repo = FileTodoRepo()
    elif storage == "sqlite":
        repo = SQLiteTodoRepo()
    else:
        raise ValueError("Invalid storage type")
    ctx.obj = TodoService(repo)

@cli.command()
@click.argument("title")
@click.option("--attachment", default="", help="Path to an image or document")
@click.pass_obj
def add(service: TodoService, title, attachment):
    """
    Add a new Todo item.
    
    :param service: The TodoService instance.
    :param title: The title of the Todo item.
    :param attachment: The path to an attachment (image or document).
    """
    todo = service.add_todo(title, attachment if attachment else None)
    click.echo(f"Added todo: {todo.id} - {todo.title}")

# Add other CLI commands

