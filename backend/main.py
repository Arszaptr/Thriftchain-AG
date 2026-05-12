from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import os

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:3002",
    "https://thriftchain-ag.vercel.app"
])

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "thriftchain-secret-key")
jwt = JWTManager(app)

users = []

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Thriftchain-AG API berjalan!"})

@app.route("/api/test")
def test():
    return jsonify({"status": "ok", "data": "Hello dari backend!"})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    nama = data.get("nama")

    if not email or not password or not nama:
        return jsonify({"status": "error", "message": "Semua field wajib diisi"}), 400

    for user in users:
        if user["email"] == email:
            return jsonify({"status": "error", "message": "Email sudah terdaftar"}), 400

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "id": len(users) + 1,
        "nama": nama,
        "email": email,
        "password": hashed,
        "token_balance": 0
    }
    users.append(user)

    return jsonify({"status": "ok", "message": "Registrasi berhasil!"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    for user in users:
        if user["email"] == email:
            if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                access_token = create_access_token(identity=str(user["id"]))
                return jsonify({
                    "status": "ok",
                    "token": access_token,
                    "user": {
                        "id": user["id"],
                        "nama": user["nama"],
                        "email": user["email"],
                        "token_balance": user["token_balance"]
                    }
                })

    return jsonify({"status": "error", "message": "Email atau password salah"}), 401

@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    for user in users:
        if user["id"] == user_id:
            return jsonify({
                "status": "ok",
                "user": {
                    "id": user["id"],
                    "nama": user["nama"],
                    "email": user["email"],
                    "token_balance": user["token_balance"]
                }
            })
    return jsonify({"status": "error", "message": "User tidak ditemukan"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)