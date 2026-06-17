import subprocess  # 1. Added subprocess import
from pathlib import Path

import typer
from rich.console import Console

console = Console()
err_console = Console(stderr=True)


# --- Templates ---

GITIGNORE_CONTENT = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
"""

MAIN_PY_CONTENT = """def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
"""


def get_readme_content(project_name: str) -> str:
    # We use a helper function so we can dynamically inject the project name
    return f"""# {project_name}

A Python project scaffolded with `pystart`.

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
   
2. Activate a virtual env:
   ```bash
   source .venv/bin/activate
   ```

## Running the project
   ```bash
   python main.py
   ```
"""


app = typer.Typer()


@app.command()
def create(project_name: str):
    """
    Scaffold a new Python project.
    """
    project_path = Path.cwd() / project_name

    if project_path.exists():
        err_console.print(
            f"[bold red]Error:[/bold red] A directory or file named '[yellow]{project_name}[/yellow]' already exists here."
        )
        raise typer.Exit(code=1)

    try:
        # Create dir
        project_path.mkdir(parents=True, exist_ok=False)
        console.print(
            f"[green]✔[/green] Created directory: [blue]{project_path}[/blue]"
        )

        # Generate README.md
        readme_path = project_path / "README.md"
        readme_path.write_text(get_readme_content(project_name), encoding="utf-8")
        console.print("[green]✔[/green] Generated: README.md")

        # Generate .gitignore
        gitignore_path = project_path / ".gitignore"
        gitignore_path.write_text(GITIGNORE_CONTENT, encoding="utf-8")
        console.print("[green]✔[/green] Generated: .gitignore")

        # Generate main.py
        main_py_path = project_path / "main.py"
        main_py_path.write_text(MAIN_PY_CONTENT, encoding="utf-8")
        console.print("[green]✔[/green] Generated: main.py")

        # Init Git Repo
        with console.status(
            "[bold blue]Initializing Git repository...", spinner="dots"
        ):
            # Run git init
            subprocess.run(
                ["git", "init"], cwd=project_path, check=True, capture_output=True
            )
            # Stage all generated files (README, main.py, .gitignore)
            subprocess.run(
                ["git", "add", "."], cwd=project_path, check=True, capture_output=True
            )
            # Create the very first commit
            subprocess.run(
                ["git", "commit", "-m", "chore: initial project scaffold"],
                cwd=project_path,
                check=True,
                capture_output=True,
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
                ["python", "-m", "venv", ".venv"],
                cwd=project_path,
                check=True,
                capture_output=True,
            )
        console.print("[green]✔[/green] Created virtual environment: .venv")

        console.print("\n[bold green] Project scaffolded successfully![/bold green]")
        console.print(
            f"To start, run:\n  [bold cyan]cd {project_name} && source .venv/bin/activate[/bold cyan]\n"
        )

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode().strip()
        err_console.print(
            f"[bold red]Error executing system command:[/bold red] {error_msg}"
        )
        raise typer.Exit(code=1)

    except Exception as e:
        err_console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
