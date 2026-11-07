# Week 2 – Python Web Application

## Project Description

This project is a Python web application running on an Ubuntu 26.04 Linux server.

The application is available at:

http://195.148.20.149/viikko2/

## Technologies Used

- Python 3
- Flask – Web application framework
- Gunicorn – WSGI application server
- Nginx – Reverse proxy
- MariaDB – Database
- systemd – Automatic service startup
- Git and GitHub – Version control

## Database and Data Storage

The application uses a MariaDB database named `appdb`.

The database contains a table called `visits`, which stores the number of page visits.

Every time the webpage is loaded, the counter increases by one. The updated value is saved in the database.

The data is stored persistently on the server, so it is not lost when the application or server restarts.

## Web Server Configuration

Nginx serves the original Week 1 website at `/`.

The Week 2 Flask application is available at `/viikko2/` through an Nginx reverse proxy.

Gunicorn runs the Python application locally on port 5000.

## Automatic Startup

Nginx, MariaDB and the Flask application are configured to start automatically when the server boots.

The Flask application runs as a systemd service named `viikko2`.

## Reboot Test

The Ubuntu server was restarted using the `sudo reboot` command.

After the restart:

- The original Week 1 website was still accessible.
- The Week 2 Flask application was accessible.
- Nginx, MariaDB and the Flask service were running.
- The visitor counter retained its previous value and continued increasing.

**Result: The reboot test was successful.**
