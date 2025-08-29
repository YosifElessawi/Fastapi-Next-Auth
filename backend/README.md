# FastAPI Todo Application

A comprehensive guide to building a FastAPI-based Todo application with PostgreSQL, SQLAlchemy, and Docker.

## Part 1: Setting up the Project 🛠️

The first step is to establish a solid foundation. This includes setting up your development environment and a clear, modular project structure.

### Create a Project Directory
Create a main folder for your project, for example, `fastapi-todo`.

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies
Install the required dependencies.

```bash
pip install -r requirements.txt
```

### Initialize the Database

```bash
alembic init migrations
```

### Start a Development Server

```bash
uvicorn app.main:app --reload
```
### Run Pre-commit

```bash
pre-commit install
```

```bash
pre-commit run --all-files
```
