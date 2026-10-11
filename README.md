Docker Microservices Learning Hub
1. Project Overview

Docker Microservices Learning Hub is a small web application for learning and documenting technologies covered in the course. It provides educational content about Docker, Docker Compose, and microservice architecture, as well as a place for users to save their own notes.

The project demonstrates containerization, service configuration, communication between containers, and persistent data storage.

2. Technologies Used
Python: Programming language used for the web application.
Flask: Python web framework used to handle HTTP requests and display pages.
Gunicorn: Application server used to run Flask inside the container.
PostgreSQL: Relational database used to store notes.
Docker: Used to package the application and database into containers.
Docker Compose: Used to configure and run the services together.
3. Architecture

The application consists of two services:

Web service

The web service runs the Flask application using Gunicorn. It displays the learning material, accepts new notes, and communicates with the PostgreSQL database.

The application is available on the host machine at http://localhost:5001.

Database service

The database service runs PostgreSQL and stores the notes submitted through the web application.

A named Docker volume stores the database files so that notes remain available when the containers are stopped and restarted.

Communication

Docker Compose creates a network for the services. The web application connects to PostgreSQL using the database service name db, rather than a manually configured IP address.

4. Running the Project

Requirements:

Docker
Docker Compose
Clone or copy the project to your computer.

Create a .env file in the project root containing:

DB_PASSWORD=replace_with_a_local_password

Build and start the services:

docker compose up --build

Open http://localhost:5001 in a browser.
Check the application's health at http://localhost:5001/health.

The health endpoint reports whether the application can communicate with the database.

To stop the services, press Ctrl+C in the terminal running Docker Compose.

To start the existing environment again, run docker compose up.

Note: The example password is for local development only. Use a strong, private password and do not commit the .env file to version control.

5. Data Persistence

PostgreSQL stores notes in a database backed by a named Docker volume. The volume allows database data to persist independently of the lifecycle of the web container.

Persistence was tested by creating a note, stopping the Docker Compose environment, starting it again, and confirming that the note remained available.

6. Health Monitoring

The /health endpoint checks whether the web application can execute a query against PostgreSQL.

healthy: the database connection works.
unhealthy: the application cannot successfully query the database.

Docker Compose also uses a PostgreSQL health check to determine when the database is ready for connections.

7. Testing

The following checks have been performed:

The web application starts successfully in Docker.
The homepage is accessible from the host machine.
The health endpoint reports a successful database connection.
Users can submit notes through the website.
Notes remain available after stopping and restarting the Compose environment.
8. Future Improvements

Possible extensions include:

Adding a separate API service.
Adding note editing and deletion.
Expanding the learning material.
Adding automated tests.
Improving monitoring and error handling.
9. Project Structure
app/: Flask application, HTML templates, CSS, and Python dependencies.
Dockerfile: Instructions for building the web application image.
compose.yaml: Configuration for the web and database services.
.env: Local environment configuration; should not be committed.
.gitignore: Files and directories excluded from version control.
docs/: Project documentation and report materials.