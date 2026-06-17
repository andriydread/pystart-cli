import typer

# Initialize the Typer application
app = typer.Typer()


@app.command()
def create(project_name: str):
    """
    Scaffold a new Python project.
    """
    print(f"Creating a new project named: {project_name}")


if __name__ == "__main__":
    app()
