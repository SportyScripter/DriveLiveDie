# Santa Clous Services

## Introduction

### Build and Run the App

1. First, make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2. Clone this repository to your local machine:
```bash
git clone https://github.com/SportyScripter/Santa_Claus_Industry
```

3. Navigate to the project directory:
```bash
cd Santa_Claus_Industry
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
### Access Fastapi Swagger UI Web Interface
You can access the Swagger by clicking [here](http://localhost:8008/docs#/).

### Access Fastapi API documentation with ReDoc
You can access the API documentation by clicking [here](http://localhost:8008/redoc).

### Access PgAdmin Web Interface
You can access the PgAdmin web interface by clicking [here](http://localhost:5050/login?next=%2F).

### PgAdmin Database Connection Information

When connecting to the database using PgAdmin, use the following connection details:

- **Host Name/Address:** db
- **Username:** Santa2137
- **Password:** Christmas420
- **Database name:** SantaDB



