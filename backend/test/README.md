# Running Tests and Generating Coverage Report

This document guides you through the process of running tests, generating a coverage report in HTML format, and viewing it in a browser using the Live Server extension in Visual Studio Code.

## Prerequisites

- Docker and Docker Compose installed on your system.
- Visual Studio Code installed on your system.
- Live Server extension for Visual Studio Code installed.

## Running Tests

To run the tests, ensure Docker containers are up and running. Then, execute the following command in your terminal:

```bash
docker-compose exec backend pytest
```

This command runs all the tests in the `backend` service using pytest.

## Generating Coverage Report in Terminal

To generate a coverage report Terminal:

```bash
docker-compose exec backend coverage report
```

This command generates a coverage report.

## Generating Coverage Report

To generate a coverage report in HTML format, you can use the pytest-cov plugin. Modify the above command as follows:

```bash
docker-compose exec backend pytest --cov=./ --cov-report html
```

This command generates a coverage report and stores it in the `htmlcov` directory within your `backend` container.

## Copying the Coverage Report to Local System

After generating the report, copy it from the Docker container to your local system using the Docker `cp` command. First, find the container ID of your backend service:

```bash
docker ps
```

Look for the `backend` service and copy its CONTAINER ID. Then, execute:

```bash
docker cp <CONTAINER_ID>:/code/htmlcov ./htmlcov
```

Replace `<CONTAINER_ID>` with your actual container ID `<drivelivedie-backend>`. This command copies the `htmlcov` directory to your local system.

## Viewing the Coverage Report

To view the HTML coverage report, use the Live Server extension in Visual Studio Code:

1. Open Visual Studio Code.
2. Navigate to the `htmlcov` directory that you've copied to your local system.
3. Find the `index.html` file, right-click on it, and select "Open with Live Server".

This will launch a local development server and open the coverage report in your default web browser.

## Installing Live Server Extension

If you haven't installed the Live Server extension in Visual Studio Code, follow these steps:

1. Open Visual Studio Code.
2. Go to the Extensions view by clicking on the square icon on the sidebar or pressing `Ctrl+Shift+X`.
3. Search for "Live Server" by Ritwick Dey.
4. Click "Install" next to the Live Server extension.

Now, you're ready to view the coverage report using Live Server as described above.
