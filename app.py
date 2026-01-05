from flask import Flask, request, jsonify
import psycopg2
import os
import bcrypt

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.route("/")
def home():
    return "API Flask funcionando 🚀"

# ---------- REGISTER ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({"error": "Usuario ya existe"}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "Usuario registrado correctamente"})

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username = %s",
        (username,)
    )
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    stored_password = user[0].encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
    return jsonify({
        "success": True,
        "message": f"Hola {username} 👋"
    })
else:
    return jsonify({
        "success": False,
        "error": "Contraseña incorrecta"
    }), 401

if __name__ == "__main__":
    app.run()
