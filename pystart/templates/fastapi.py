# pystart/templates/fastapi.py

# FastAPI doesn't need a special gitignore, we can reuse the same one
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

# The requirements for a basic FastAPI app
REQUIREMENTS_CONTENT = """fastapi
uvicorn
"""

MAIN_PY_CONTENT = """from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from your FastAPI app!"}
"""


def get_readme_content(project_name: str) -> str:
    return f"""# {project_name} (FastAPI)

A web API scaffolded with `pystart`.

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
   
2. Activate a virtual env:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API
   ```bash
   uvicorn main:app --reload
   ```
   Your app will be running at http://127.0.0.1:8000
"""
