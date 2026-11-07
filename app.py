
from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)


# Yhteys MariaDB-tietokantaan
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'appdb')
    )


# Etusivu ja kävijälaskuri
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kasvatetaan kävijämäärää yhdellä
    cursor.execute(
        "UPDATE visits SET count = count + 1 WHERE id = 1"
    )

    conn.commit()

    # Haetaan päivitetty kävijämäärä
    cursor.execute("SELECT count FROM visits WHERE id = 1")
    visits = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return f"""
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Viikko 2 - Python-verkkosovellus</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #eef2f7;
                color: #243247;
                margin: 0;
                padding: 40px 20px;
            }}

            .container {{
                max-width: 750px;
                margin: auto;
                background: white;
                padding: 35px;
                border-radius: 15px;
                box-shadow: 0 4px 15px #00000015;
            }}

            h1 {{
                color: #2457a7;
            }}

            .counter {{
                background: #2457a7;
                color: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                margin: 25px 0;
            }}

            .number {{
                font-size: 48px;
                font-weight: bold;
            }}

            a {{
                color: #2457a7;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Python-verkkosovellus</h1>

            <p>
                Tervetuloa viikon 2 verkkosovellukseen!
                Tämä sivu on toteutettu Pythonilla ja Flaskilla.
            </p>

            <div class="counter">
                <div>Sivun käyntikerrat</div>
                <div class="number">{visits}</div>
            </div>

            <h2>Toteutuksen tiedot</h2>

            <ul>
                <li>Ohjelmointikieli: Python 3</li>
                <li>Web-sovellus: Flask</li>
                <li>Palvelin: Gunicorn ja Nginx</li>
                <li>Tietokanta: MariaDB</li>
            </ul>

            <h2>Kävijälaskuri ja tietokanta</h2>

            <p>
                Kävijälaskuri kasvattaa käyntimäärää yhdellä
                jokaisella sivun latauksella. Käyntimäärä
                tallennetaan MariaDB-tietokantaan visits-tauluun.
                Tämän ansiosta laskuri säilyy myös palvelimen
                uudelleenkäynnistyksen jälkeen.
            </p>

            <h2>Uudelleenkäynnistystesti</h2>

            <p>
                Uudelleenkäynnistystesti suoritetaan sovelluksen
                julkaisemisen jälkeen.
            </p>

            <h2>GitHub</h2>

            <p>
                <a href="GITHUB_LINKKI">
                    Projektin lähdekoodi GitHubissa
                </a>
            </p>

        </div>
    </body>
    </html>
    """


# Health check
@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})


# Käyttäjien hakeminen tietokannasta
@app.route('/api/users')
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Kehityskäyttö
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
