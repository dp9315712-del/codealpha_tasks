from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import secrets
import string
from urllib.parse import urlparse

app = Flask(__name__)

DATABASE = "database.db"


# Connect to database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Generate unique short code
def generate_short_code():
    characters = string.ascii_letters + string.digits

    return ''.join(
        secrets.choice(characters) for _ in range(6)
    )


# Validate URL
def is_valid_url(url):
    try:
        parsed_url = urlparse(url)

        return (
            parsed_url.scheme in ["http", "https"]
            and parsed_url.netloc != ""
        )

    except Exception:
        return False


# Home page
@app.route("/", methods=["GET", "POST"])
def home():

    short_url = None
    error = None

    if request.method == "POST":

        original_url = request.form.get("original_url", "").strip()

        if not is_valid_url(original_url):

            error = "Please enter a valid URL starting with http:// or https://"

        else:

            conn = get_db_connection()

            # Generate unique short code
            while True:

                short_code = generate_short_code()

                existing_url = conn.execute(
                    "SELECT id FROM urls WHERE short_code = ?",
                    (short_code,)
                ).fetchone()

                if existing_url is None:
                    break

            # Save URL in database
            conn.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                (original_url, short_code)
            )

            conn.commit()
            conn.close()

            short_url = request.host_url + short_code

    return render_template(
        "index.html",
        short_url=short_url,
        error=error
    )


# API to create short URL
@app.route("/api/shorten", methods=["POST"])
def create_short_url_api():

    data = request.get_json(silent=True) or {}

    original_url = data.get("original_url", "").strip()

    if not is_valid_url(original_url):

        return jsonify({
            "error": "Please enter a valid URL"
        }), 400

    conn = get_db_connection()

    while True:

        short_code = generate_short_code()

        existing_url = conn.execute(
            "SELECT id FROM urls WHERE short_code = ?",
            (short_code,)
        ).fetchone()

        if existing_url is None:
            break

    conn.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code)
    )

    conn.commit()
    conn.close()

    short_url = request.host_url + short_code

    return jsonify({
        "original_url": original_url,
        "short_code": short_code,
        "short_url": short_url
    }), 201

# Redirect to original URL
@app.route("/<short_code>")
def redirect_url(short_code):

    conn = get_db_connection()

    url_data = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    if url_data:

        return redirect(url_data["original_url"], code=302)

    return "Short URL not found!", 404


# Start server
if __name__ == "__main__":

    create_table()

    app.run(debug=True)
