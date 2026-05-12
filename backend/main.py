from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:3002",
    "https://thriftchain-ag.vercel.app"
])

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Thriftchain-AG API berjalan!"})

@app.route("/api/test")
def test():
    return jsonify({"status": "ok", "data": "Hello dari backend!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)