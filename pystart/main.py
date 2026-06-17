import subprocess  # 1. Added subprocess import
from pathlib import Path

import typer

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
        typer.echo(
            f"Error: A directory or file named '{project_name}' already exists here.",
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        # 1. Create directory
        project_path.mkdir(parents=True, exist_ok=False)
        typer.echo(f"Successfully created directory: {project_path}")

        # 2. Generate README.md
        readme_path = project_path / "README.md"
        readme_path.write_text(get_readme_content(project_name), encoding="utf-8")
        typer.echo("Generated: README.md")

        # 3. Generate .gitignore
        gitignore_path = project_path / ".gitignore"
        gitignore_path.write_text(GITIGNORE_CONTENT, encoding="utf-8")
        typer.echo("Generated: .gitignore")

        # 4. Generate main.py
        main_py_path = project_path / "main.py"
        main_py_path.write_text(MAIN_PY_CONTENT, encoding="utf-8")
        typer.echo("Generated: main.py")

        # 5. Initialize Git Repository
        typer.echo("Initializing Git repository...")
        # Passing the command as a list protects against shell injection vulnerabilities
        subprocess.run(
            ["git", "init"], cwd=project_path, check=True, capture_output=True
        )
        typer.echo("Initialized Git repository.")

        # 6. Create Virtual Environment
        typer.echo("Creating virtual environment (this may take a few seconds)...")
        subprocess.run(
            ["python", "-m", "venv", ".venv"],
            cwd=project_path,
            check=True,
            capture_output=True,
        )
        typer.echo("Created virtual environment: .venv")

    except subprocess.CalledProcessError as e:
        # Decoding the binary stderr output back into a readable string
        error_msg = e.stderr.decode().strip()
        typer.echo(f"Error executing system command: {error_msg}", err=True)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
