import click
from presentation.cli import cli  # Assuming your CLI commands are defined here
from presentation.flet_ui import main as flet_main
import flet as ft

@click.group()
def main():
    """Todo List Application"""
    pass

@main.command()
def gui():
    """Run the Flet GUI"""
    print("Starting Flet GUI...")
    ft.app(target=flet_main, host="0.0.0.0", port=8550, view=ft.WEB_BROWSER)

main.add_command(cli, name="cli")

if __name__ == "__main__":
    main()
