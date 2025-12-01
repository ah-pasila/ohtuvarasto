# ohtuvarasto

[![Worklow badge](https://github.com/ah-pasila/ohtuvarasto/actions/workflows/main.yml/badge.svg?)](https://github.com/ah-pasila/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/ah-pasila/ohtuvarasto/graph/badge.svg?token=TE8LBUBNLY)](https://codecov.io/github/ah-pasila/ohtuvarasto)

## Installation

1. Install Poetry if you haven't already:
```bash
pip install poetry
```

2. Install project dependencies:
```bash
poetry install
```

## Usage

### Running the Web Application

```bash
cd src
poetry run python app.py
```

Or using Flask CLI:
```bash
cd src
FLASK_APP=app.py poetry run flask run
```

The application will be available at `http://127.0.0.1:5000/`

### Running Tests

```bash
poetry run pytest src/tests
```

### Running Pylint

```bash
poetry run pylint src
```

### Running Coverage

```bash
poetry run coverage run --branch -m pytest
poetry run coverage report
```
