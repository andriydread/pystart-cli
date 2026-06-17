# pystart

CLI tool to quickly scaffold new Python projects.

## What it does

- Creates your project folder.
- Generates standard boilerplate files (`main.py`, `.gitignore`, `README.md`).
- Initializes a local Git repository and makes an initial commit.
- Creates an isolated virtual environment (`.venv`).
- **Safe Cleanup:** If any setup step fails, it automatically deletes the partially created project folder to keep your directory clean.

## Prerequisites

Before installing, make sure you have the following on your system:

- **Python 3.8+**
- **Git**

## Installation

The recommended way to install `pystart` globally is using **pipx** (which keeps the tool's dependencies isolated from your system Python):

```bash
# Clone this repository
git clone https://github.com/andriydread/pystart-cli.git
cd pystart-cli

# Install globally in editable mode (changes you make to the code will apply instantly)
pipx install -e .
```

_(If you do not use `pipx`, you can run `pip install --user -e .` from the project directory instead)._

## Usage

You can run `pystart` from any directory on your computer:

```bash
pystart my-new-project
```

### Generated Structure

The tool will automatically build this structure:

```text
my-new-project/
├── .git/
├── .venv/
├── .gitignore
├── README.md
└── main.py
```

### Next Steps

Once scaffolding is complete, simply run:

```bash
cd my-new-project && source .venv/bin/activate
python main.py
```
