from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def create(project_name: str):
    """
    Scaffold a new Python project.
    """
    # Resolve the path where the project should be created
    project_path = Path.cwd() / project_name

    #  Path Validation
    if project_path.exists():
        typer.echo(
            f"Error: A directory or file named '{project_name}' already exists here.",
            err=True,
        )
        raise typer.Exit(code=1)

    # Directory Creation
    try:
        project_path.mkdir(parents=True, exist_ok=False)
        typer.echo(f"Successfully created directory: {project_path}")
    except Exception as e:
        typer.echo(
            f"An unexpected error occurred while creating the directory: {e}", err=True
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
