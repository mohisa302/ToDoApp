# ToDoApp

ToDoApp is a versatile application for managing your tasks with support for attachments. It offers both a graphical user interface (GUI) using Flet and a command-line interface (CLI) for different storage backends (in-memory, file, SQLite).

## Features

- Add, edit, and delete tasks
- Attach files (images, PDFs) to tasks
- View tasks with attachments
- Multiple storage options: in-memory, file, SQLite
- GUI and CLI interfaces

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/ToDoApp.git
   cd ToDoApp
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### GUI

To run the GUI version of the app:

```sh
python main.py gui
```

The app will be accessible in your web browser at `http://0.0.0.0:8550`.

### CLI

To use the CLI, you can run the following commands:

```sh
python main.py cli --help
```

#### Adding a Task

```sh
python main.py cli add "New Task" --attachment /path/to/file
```

## Docker

You can also run the application using Docker. Ensure you have Docker installed and running on your machine.

1. Build and start the services:

   ```sh
   docker-compose up --build
   ```

2. The GUI will be available at `http://0.0.0.0:8550`.

## Configuration

The application supports different storage backends. You can configure the storage type using the `--storage` option in the CLI or by modifying the `TodoService` initialization in the GUI code.

### Storage Options

- `memory`: In-memory storage (default)
- `file`: File-based storage
- `sqlite`: SQLite database storage

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flet](https://flet.dev/) for the GUI framework
- [Click](https://click.palletsprojects.com/) for the CLI framework
