from flask import Flask, request
import os
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "learninghub")
DB_USER = os.environ.get("DB_USER", "learninguser")
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ.get("DB_PORT", "5432")


def get_db():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        row_factory=dict_row
    )


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                title VARCHAR(120) NOT NULL,
                content VARCHAR(5000) NOT NULL
            )
        """)


@app.route("/health")
def health():
    try:
        with get_db() as db:
            db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except psycopg.Error:
        return {"status": "unhealthy", "database": "disconnected"}, 503


@app.route("/notes", methods=["GET"])
def get_notes():
    with get_db() as db:
        notes = db.execute(
            "SELECT * FROM notes ORDER BY id DESC"
        ).fetchall()

    return notes


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}, 400

    title = data.get("title", "")
    content = data.get("content", "")

    if not isinstance(title, str) or not isinstance(content, str):
        return {"error": "Title and content must be text"}, 400

    title = title.strip()
    content = content.strip()

    if not title or not content:
        return {"error": "Title and content are required"}, 400

    if len(title) > 120 or len(content) > 5000:
        return {"error": "Title or content is too long"}, 400

    with get_db() as db:
        note = db.execute(
            """
            INSERT INTO notes (title, content)
            VALUES (%s, %s)
            RETURNING id, title, content
            """,
            (title, content)
        ).fetchone()

    return note, 201


init_db()