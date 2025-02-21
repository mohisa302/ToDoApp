import flet as ft
import base64
import mimetypes
import functools
from application.services import TodoService
from infrastructure.sqlite_repo import SQLiteTodoRepo  # Using SQLite for attachments

class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        # Use SQLite repo so attachments are stored in the database
        self.service = TodoService(SQLiteTodoRepo())
        self.page.title = "Todo App"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.window_width = 500
        self.page.window_height = 700
        # Variables for new task and edit attachments
        self.attachment_file = None        
        self.edit_attachment_file = None   
        self.main_ui()

    def main_ui(self):
        self.new_task = ft.TextField(hint_text="What needs to be done?", expand=True)
        # Create file pickers for new tasks and edits
        self.attach_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.edit_attach_picker = ft.FilePicker(on_result=self.on_edit_file_picked)
        self.page.overlay.append(self.attach_picker)
        self.page.overlay.append(self.edit_attach_picker)
        self.tasks_view = ft.ListView(expand=True, spacing=10)
        # Always add a visible Column to the page
        self.page.controls = [
            ft.Column([
                ft.Row([
                    self.new_task,
                    ft.IconButton(
                        icon=ft.icons.FOLDER_OPEN,
                        on_click=self.pick_file,
                        tooltip="Pick an attachment"
                    ),
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        on_click=self.add_task,
                        tooltip="Add Task"
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Text("Your Tasks:", size=20, weight=ft.FontWeight.BOLD),
                self.tasks_view
            ], expand=True)
        ]
        self.load_tasks()
        self.page.update()

    def pick_file(self, e):
        self.attach_picker.pick_files(allow_multiple=False)

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            if file.size > 5 * 1024 * 1024:
                self.show_error("File is too large (max 5MB)")
                return
            # For web mode, file.content is base64 encoded
            if hasattr(file, "content") and file.content:
                attachment_data = base64.b64decode(file.content)
            elif file.path:
                with open(file.path, "rb") as f:
                    attachment_data = f.read()
            else:
                attachment_data = None
            if attachment_data:
                attachment_filename = file.name
                attachment_mimetype, _ = mimetypes.guess_type(file.name)
                self.attachment_file = {
                    "data": attachment_data,
                    "name": attachment_filename,
                    "mimetype": attachment_mimetype
                }
                self.show_success(f"Selected for new task: {attachment_filename}")
            else:
                self.show_error("Failed to load file")
            self.page.update()

    def edit_pick_file(self, e):
        self.edit_attach_picker.pick_files(allow_multiple=False)

    def on_edit_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            if file.size > 5 * 1024 * 1024:
                self.show_error("File is too large (max 5MB)")
                return
            if hasattr(file, "content") and file.content:
                attachment_data = base64.b64decode(file.content)
            elif file.path:
                with open(file.path, "rb") as f:
                    attachment_data = f.read()
            else:
                attachment_data = None
            if attachment_data:
                attachment_filename = file.name
                attachment_mimetype, _ = mimetypes.guess_type(file.name)
                self.edit_attachment_file = {
                    "data": attachment_data,
                    "name": attachment_filename,
                    "mimetype": attachment_mimetype
                }
                self.show_success(f"Selected for edit: {attachment_filename}")
            else:
                self.show_error("Failed to load file for edit")
            self.page.update()

    def add_task(self, e):
        if self.new_task.value.strip():
            try:
                if self.attachment_file:
                    self.service.add_todo(
                        self.new_task.value,
                        attachment_data=self.attachment_file["data"],
                        attachment_filename=self.attachment_file["name"],
                        attachment_mimetype=self.attachment_file["mimetype"]
                    )
                    self.show_success("Task added with attachment successfully.")
                    self.attachment_file = None
                else:
                    self.service.add_todo(self.new_task.value)
                    self.show_success("Task added successfully.")
            except Exception as err:
                self.show_error(str(err))
            self.new_task.value = ""
            self.load_tasks()
            self.page.update()

    def load_tasks(self):
      self.tasks_view.controls = []
      for todo in self.service.list_todos():
          card_children = [
              ft.Row([
                  ft.Checkbox(
                      value=todo.completed,
                      on_change=lambda e, tid=todo.id: self.toggle_complete(tid, e)
                  ),
                  ft.Text(todo.title, expand=True),
              ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
          ]
          if todo.attachment_data:
              if todo.attachment_mimetype and todo.attachment_mimetype.startswith("image/"):
                  encoded = base64.b64encode(todo.attachment_data).decode("utf-8")
                  image_src = f"data:{todo.attachment_mimetype};base64,{encoded}"
                  card_children.append(ft.Image(src=image_src, width=200, height=200))
              elif todo.attachment_mimetype == "application/pdf":
                  card_children.append(ft.Text(f"PDF attached: {todo.attachment_filename}"))
              card_children.append(
                  ft.ElevatedButton(
                      "Download Attachment",
                      on_click=lambda e, t=todo: self.download_attachment(t, e)
                  )
              )
          card_children.append(
              ft.Row([
                  ft.IconButton(
                      icon=ft.icons.EDIT,
                      tooltip="Edit Task",
                      on_click=lambda e, t=todo: self.edit_task(t, e)
                  ),
                  ft.IconButton(
                      icon=ft.icons.DELETE,
                      tooltip="Delete Task",
                      on_click=lambda e, tid=todo.id: self.delete_task(tid, e)
                  ),
              ], alignment=ft.MainAxisAlignment.END, spacing=10)
          )
          self.tasks_view.controls.append(
              ft.Card(
                  content=ft.Container(
                      content=ft.Column(card_children, spacing=10),
                      padding=10,
                  )
              )
          )
      self.page.update()

    def toggle_complete(self, todo_id, e):
        todo = self.service.repository.get(todo_id)
        self.service.update_todo(todo_id, completed=not todo.completed)
        self.load_tasks()

    def edit_task(self, todo, e=None):
        # Debug: confirm edit is triggered
        self.show_success(f"Editing task: {todo.title}")
        # Store the todo being edited and reset previous edit file
        self.edit_dialog_todo = todo  
        self.edit_attachment_file = None  
        edit_field = ft.TextField(value=todo.title, expand=True)
        dialog = ft.AlertDialog(
            title=ft.Text("Edit Task"),
            content=ft.Column([
                ft.Text("New title:"),
                edit_field,
                ft.Text("To update attachment, click below:"),
                ft.ElevatedButton("Pick File", on_click=self.edit_pick_file)
            ]),
            actions=[
                ft.TextButton("Save", on_click=lambda e: self.save_edit(edit_field.value, dialog)),
                ft.TextButton("Cancel", on_click=lambda e: self.close_edit_dialog(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def save_edit(self, new_title, dialog):
        # Use new attachment if selected; otherwise, use existing one
        if self.edit_attachment_file:
            filename = self.edit_attachment_file["name"]
            mimetype = self.edit_attachment_file["mimetype"]
            data = self.edit_attachment_file["data"]
        else:
            filename = self.edit_dialog_todo.attachment_filename
            mimetype = self.edit_dialog_todo.attachment_mimetype
            data = self.edit_dialog_todo.attachment_data
        try:
            self.service.update_todo(
                self.edit_dialog_todo.id,
                title=new_title,
                attachment_filename=filename,
                attachment_mimetype=mimetype,
                attachment_data=data
            )
            self.show_success("Task updated successfully!")
        except Exception as err:
            self.show_error(str(err))
        dialog.open = False
        self.load_tasks()
        self.page.update()

    def close_edit_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def delete_task(self, todo_id, e):
        self.service.delete_todo(todo_id)
        self.show_success("Task deleted successfully.")
        self.load_tasks()
        self.page.update()

    def download_attachment(self, todo, e):
        if todo.attachment_data:
            encoded = base64.b64encode(todo.attachment_data).decode("utf-8")
            data_url = f"data:{todo.attachment_mimetype};base64,{encoded}"
            ft.launch_url(data_url)
            self.show_success("Download started.")
            self.page.update()

    def show_success(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.GREEN_200), bgcolor=ft.colors.GREY_900)
        self.page.snack_bar.open = True
        self.page.update()

    def show_error(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.RED_200), bgcolor=ft.colors.GREY_900)
        self.page.snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    TodoApp(page)

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8550, view=ft.WEB_BROWSER)
