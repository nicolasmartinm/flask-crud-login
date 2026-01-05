import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Railway inyecta esta variable automáticamente
DATABASE_URL = os.environ.get("DATABASE_URL")

# ---------- CONEXIÓN A LA DB ----------
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# ---------- RUTA DE PRUEBA ----------
@app.route("/")
def home():
    return "🔥 Flask + PostgreSQL funcionando en Railway"

# ---------- REGISTRO ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        return jsonify({"message": "Usuario creado correctamente"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Usuario ya existe"}), 400
    finally:
        cur.close()
        conn.close()

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username = %s AND password = %s",
        (username, password)
    )

    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"message": f"Hola {username} 👋"}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
