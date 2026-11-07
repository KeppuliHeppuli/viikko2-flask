from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'appdb')
    )


@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Increase the visitor counter
    cursor.execute(
        "UPDATE visits SET count = count + 1 WHERE id = 1"
    )
    conn.commit()

    # Get the current visitor count
    cursor.execute(
        "SELECT count FROM visits WHERE id = 1"
    )
    visits = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Week 2 - Python Web Application</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f4f8;
                margin: 0;
                padding: 40px 20px;
                text-align: center;
            }}

            .container {{
                background: white;
                max-width: 700px;
                margin: auto;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2563eb;
            }}

            h2 {{
                color: #333;
            }}

            p {{
                color: #555;
                line-height: 1.6;
            }}

            .counter {{
                font-size: 36px;
                font-weight: bold;
                color: #2563eb;
                margin: 20px 0;
            }}

            a {{
                color: #2563eb;
                text-decoration: none;
                font-weight: bold;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Week 2 - Python Web Application</h1>

            <p>
                Welcome to my Week 2 Linux server project!
            </p>

            <h2>About This Project</h2>

            <p>
                This website is running on an Ubuntu Linux server.
                The application is built with Python and Flask.
                Nginx works as a reverse proxy, and Gunicorn
                runs the Python application.
            </p>

            <h2>Visitor Counter</h2>

            <p>
                This page has been visited:
            </p>

            <div class="counter">
                {visits} times
            </div>

            <p>
                The visitor counter is stored in a MariaDB database.
                Each page load increases the counter by one.
            </p>

            <h2>Database and Storage</h2>

            <p>
                The application uses MariaDB to store visitor data.
                The information is saved permanently and is not
                lost when the server restarts.
            </p>

            <h2>Automatic Startup</h2>

            <p>
                Nginx, MariaDB and the Flask application start
                automatically when the Ubuntu server boots.
            </p>

            <h2>Server Reboot Test</h2>

            <p>
                I restarted the server and verified that the
                website was still accessible and the visitor
                counter retained its previous value.
            </p>

            <h2>GitHub Repository</h2>

            <p>
                You can view the source code on GitHub:
            </p>

            <p>
                <a href="https://github.com/KeppuliHeppuli/viikko2-flask"
                   target="_blank" rel="noopener noreferrer">
                    View Project on GitHub
                </a>
            </p>

        </div>
    </body>
    </html>
    """


@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
