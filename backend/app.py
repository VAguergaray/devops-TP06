from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import datetime

app = Flask(__name__)
CORS(app)


def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "notes"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
    )


@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_conn()
        conn.close()
        db_status = "ok"
    except Exception:
        db_status = "error"

    return jsonify({
        "status": "ok",
        "database": db_status,
        "time": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })


@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, content, created_at "
        "FROM notes ORDER BY created_at DESC"
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "title": r[1],
            "content": r[2],
            "created_at": str(r[3])
        }
        for r in rows
    ])


@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()

    if not title:
        return jsonify({"error": "El título es obligatorio"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
        (title, data.get("content", ""))
    )

    note_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": note_id,
        "message": "nota creada"
    }), 201


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "nota eliminada"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
