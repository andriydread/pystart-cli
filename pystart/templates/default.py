# pystart/templates/default.py

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
