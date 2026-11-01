import json
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]}})

MENU = json.loads((Path(__file__).resolve().parent.parent / "menu.json").read_text(encoding="utf-8"))
DRINKS = json.loads((Path(__file__).resolve().parent.parent / "drinks.json").read_text(encoding="utf-8"))


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Kutak API"})


@app.get("/api/menu")
def get_menu():
    return jsonify(MENU)


@app.get("/api/drinks")
def get_drinks():
    return jsonify(DRINKS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
