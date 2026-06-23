import shutil
import subprocess
import sys
from enum import Enum
from pathlib import Path

import typer
from rich.console import Console

from .templates import default, fastapi

console = Console()
err_console = Console(stderr=True)


# Define choices as an Enum
class TemplateChoice(str, Enum):
    default = "default"
    fastapi = "fastapi"


# Map Enum choices directly to the imported modules
TEMPLATE_MAP = {
    TemplateChoice.default: default,
    TemplateChoice.fastapi: fastapi,
}

app = typer.Typer()


@app.command()
def create(
    project_name: str,
    template: TemplateChoice = typer.Option(
        TemplateChoice.default, "--template", "-t", help="The project template to use"
    ),
):
    """
    Scaffold a new Python project.
    """
    project_path = Path.cwd() / project_name

    if project_path.exists():
        err_console.print(
            f"[bold red]Error:[/bold red] A directory or file named '[yellow]{project_name}[/yellow]' already exists here."
        )
        raise typer.Exit(code=1)

    dir_created = False

    try:
        # Dynamically fetch the selected template module
        selected_template = TEMPLATE_MAP[template]

        # Create directory
        project_path.mkdir(parents=True, exist_ok=False)
        dir_created = True
        console.print(
            f"[green]✔[/green] Created directory: [blue]{project_path}[/blue]"
        )

        # Generate README.md
        readme_path = project_path / "README.md"
        readme_path.write_text(
            selected_template.get_readme_content(project_name), encoding="utf-8"
        )
        console.print("[green]✔[/green] Generated: README.md")

        # Generate .gitignore
        gitignore_path = project_path / ".gitignore"
        gitignore_path.write_text(selected_template.GITIGNORE_CONTENT, encoding="utf-8")
        console.print("[green]✔[/green] Generated: .gitignore")

        # Generate main.py
        main_py_path = project_path / "main.py"
        main_py_path.write_text(selected_template.MAIN_PY_CONTENT, encoding="utf-8")
        console.print("[green]✔[/green] Generated: main.py")

        # Generate requirements.txt (Only if the template has it defined)
        if hasattr(selected_template, "REQUIREMENTS_CONTENT"):
            requirements_path = project_path / "requirements.txt"
            requirements_path.write_text(
                selected_template.REQUIREMENTS_CONTENT, encoding="utf-8"
            )
            console.print("[green]✔[/green] Generated: requirements.txt")

        # Init Git Repo and First Commit
        with console.status(
            "[bold blue]Initializing Git repository...", spinner="dots"
        ):
            subprocess.run(
                ["git", "init"], cwd=project_path, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "add", "."], cwd=project_path, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", "chore: initial project scaffold"],
                cwd=project_path,
                check=True,
                capture_output=True,
                text=True,
            )
        console.print(
            "[green]✔[/green] Initialized Git repository and created initial commit."
        )

        # Create venv
        with console.status(
            "[bold cyan]Creating virtual environment (this may take a few seconds)...",
            spinner="dots",
        ):
            subprocess.run(
                [sys.executable, "-m", "venv", ".venv"],
                cwd=project_path,
                check=True,
                capture_output=True,
                text=True,
            )
        console.print("[green]✔[/green] Created virtual environment: .venv")

        console.print("\n[bold green]🎉 Project scaffolded successfully![/bold green]")

        # Display instructions depending on the chosen template
        if template == TemplateChoice.fastapi:
            console.print(
                f"To start your API, run:\n  [bold cyan]cd {project_name} && source .venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload[/bold cyan]\n"
            )
        else:
            console.print(
                f"To start, run:\n  [bold cyan]cd {project_name} && source .venv/bin/activate && python main.py[/bold cyan]\n"
            )

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        err_console.print(
            f"[bold red]Error executing system command:[/bold red] {error_msg}"
        )

        if dir_created and project_path.exists():
            shutil.rmtree(project_path)
            err_console.print(
                f"[yellow]⚠ Scaffolding failed[/yellow]. Cleaned up partial directory: [blue]{project_path}[/blue]"
            )

        raise typer.Exit(code=1)

    except Exception as e:
        err_console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")

        if dir_created and project_path.exists():
            shutil.rmtree(project_path)
            err_console.print(
                f"[yellow]⚠ Scaffolding failed[/yellow]. Cleaned up partial directory: [blue]{project_path}[/blue]"
            )

        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
