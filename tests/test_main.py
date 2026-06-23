import subprocess
from unittest.mock import patch

from typer.testing import CliRunner

from pystart.main import app

runner = CliRunner()


def test_create_project_success(tmp_path, monkeypatch):
    """
    Test that creating a project with the default template succeeds and generates all files.
    """
    # 2. Use monkeypatch to temporarily change the current working directory to our Pytest temp folder
    monkeypatch.chdir(tmp_path)

    # 3. Execute the command (mimicking: pystart my-test-project)
    result = runner.invoke(app, ["my-test-project"])

    # 4. Verify the CLI command exited successfully (code 0)
    assert result.exit_code == 0
    assert "Created directory" in result.stdout
    assert "Project scaffolded successfully!" in result.stdout

    # 5. Verify the files were physically created inside the temporary path
    project_dir = tmp_path / "my-test-project"

    assert project_dir.exists()
    assert (project_dir / "main.py").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / ".gitignore").exists()

    # 6. Verify that "requirements.txt" was NOT created (since this is the default template)
    assert not (project_dir / "requirements.txt").exists()


def test_create_project_already_exists(tmp_path, monkeypatch):
    """
    Test that trying to create a project in an existing folder fails cleanly.
    """
    monkeypatch.chdir(tmp_path)

    # Manually create a duplicate directory first
    existing_dir = tmp_path / "duplicate-project"
    existing_dir.mkdir()

    # Try to scaffold a project with the same name
    result = runner.invoke(app, ["duplicate-project"])

    # Verify it exits with code 1 and outputs our error message
    assert result.exit_code == 1
    assert "already exists here" in result.output


def test_create_project_fastapi_template(tmp_path, monkeypatch):
    """
    Test that selecting the fastapi template generates requirements.txt and API code.
    """
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["web-api", "--template", "fastapi"])

    assert result.exit_code == 0
    project_dir = tmp_path / "web-api"

    # Verify FastAPI-specific files exist
    assert (project_dir / "requirements.txt").exists()
    assert "from fastapi import FastAPI" in (project_dir / "main.py").read_text(
        encoding="utf-8"
    )


def test_create_project_rollback_on_failure(tmp_path, monkeypatch):
    """
    Test that if a system command fails, the project directory is cleaned up.
    """
    monkeypatch.chdir(tmp_path)

    # We "patch" subprocess.run to force it to raise a CalledProcessError
    with patch("pystart.main.subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="git init", stderr="Fake system command crash"
        )

        result = runner.invoke(app, ["doomed-project"])

        # Verify it caught the error and exited with code 1
        assert result.exit_code == 1

        # TRANSACTIONAL ASSERTION: Verify the directory was actually deleted!
        doomed_dir = tmp_path / "doomed-project"
        assert not doomed_dir.exists()
