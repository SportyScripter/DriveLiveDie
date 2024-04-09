# DriveLiveDie Services

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![DigitalOcean](https://img.shields.io/badge/Digital_Ocean-0080FF?style=for-the-badge&logo=DigitalOcean&logoColor=white)

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Docker CI](https://github.com/SportyScripter/DriveLiveDie/actions/workflows/ci-cd-pipeline.yaml/badge.svg)](https://github.com/SportyScripter/DriveLiveDie/actions/workflows/ci-cd-pipeline.yaml)

[![codecov](https://codecov.io/github/SportyScripter/DriveLiveDie/graph/badge.svg?token=119X24X6GZ)](https://codecov.io/github/SportyScripter/DriveLiveDie)

# Technologies

- **Python**
- **Docker**
- **FastAPI**
- **Postgresql**
- **React**

## Introduction

### Build and Run the App

1. First, make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2. Clone this repository to your local machine:

```bash
git clone https://github.com/SportyScripter/DriveLiveDie
```

3. Navigate to the project directory:

```bash
cd DriveLiveDie
```

4. It's recommended to use a virtual environment to manage dependencies. If you haven't installed `virtualenv` yet, you can do so using pip:

```bash
pip install virtualenv
```

5. Create a virtual environment:

```bash
virtualenv venv
```

6. Activate the virtual environment. On Windows:

```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

7. To build the app for the first timec, run:

```bash
docker-compose up --build
```

8. To start the app (after the initial build), use:

```bash
docker-compose up
```

8. To start Test:

```bash
docker-compose exec backend pytest
```

### Access Fastapi Swagger UI Web Interface

You can access the Swagger by clicking [here](http://localhost:8008/docs#/).

### Access Fastapi API documentation with ReDoc

You can access the API documentation by clicking [here](http://localhost:8008/redoc).

### Access PgAdmin Web Interface

You can access the PgAdmin web interface by clicking [here](http://localhost:5050/login?next=%2F).

### PgAdmin Database Connection Information

When connecting to the database using PgAdmin, use the following connection details:

- **Host Name/Address:** db
- **Username:** GhostRider
- **Password:** Devil666
- **Database name:** DriveLiveDieApp
