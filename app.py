from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg": "Usuario registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return jsonify({"msg": "Login exitoso"}), 200
    else:
        return jsonify({"msg": "Credenciales incorrectas"}), 401


@app.route("/")
def home():
    return "API Flask funcionando 🚀"
