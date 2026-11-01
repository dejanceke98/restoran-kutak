from datetime import datetime
from email.message import EmailMessage
from itertools import count
import json
import os
from pathlib import Path
import smtplib
import ssl

from dotenv import load_dotenv
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

reservations = []
reservation_ids = count(1)

MENU = json.loads((Path(__file__).resolve().parent.parent / "menu.json").read_text(encoding="utf-8"))


def send_reservation_email(reservation):
    host = os.getenv("SMTP_HOST", "").strip()
    username = os.getenv("SMTP_USERNAME", "").strip()
    password = os.getenv("SMTP_PASSWORD", "")
    sender = os.getenv("SMTP_FROM", username).strip()
    recipient = os.getenv("RESERVATION_EMAIL", "").strip()
    missing_settings = [
        name for name, value in (
            ("SMTP_HOST", host),
            ("SMTP_USERNAME", username),
            ("SMTP_PASSWORD", password),
            ("SMTP_FROM", sender),
            ("RESERVATION_EMAIL", recipient),
        ) if not value
    ]
    if missing_settings:
        raise RuntimeError(f"Nedostaju SMTP podešavanja: {', '.join(missing_settings)}")

    message = EmailMessage()
    message["Subject"] = f"Nova rezervacija Kutak #{reservation['id']}"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "Primljena je nova rezervacija preko sajta Kutak.\n\n"
        f"Ime: {reservation['name']}\n"
        f"Telefon: {reservation['phone']}\n"
        f"Datum: {reservation['date']}\n"
        f"Vreme: {reservation['time']}\n"
        f"Broj osoba: {reservation['guests']}\n"
        f"Napomena: {reservation['note'] or 'Nema'}\n"
    )

    port = int(os.getenv("SMTP_PORT", "587"))
    use_ssl = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
    tls_context = ssl.create_default_context()
    if use_ssl:
        with smtplib.SMTP_SSL(host, port, context=tls_context, timeout=15) as server:
            server.login(username, password)
            server.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.ehlo()
            server.starttls(context=tls_context)
            server.ehlo()
            server.login(username, password)
            server.send_message(message)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Kutak API"})


@app.get("/api/menu")
def get_menu():
    return jsonify(MENU)


@app.post("/api/reservations")
def create_reservation():
    data = request.get_json(silent=True) or {}
    required = ("name", "phone", "date", "time", "guests")
    missing = [field for field in required if not str(data.get(field, "")).strip()]
    if missing:
        return jsonify({"error": "Popunite sva obavezna polja."}), 400

    try:
        guests = int(data["guests"])
        datetime.strptime(data["date"], "%Y-%m-%d")
    except (TypeError, ValueError):
        return jsonify({"error": "Proverite datum i broj gostiju."}), 400

    if not 1 <= guests <= 12:
        return jsonify({"error": "Rezervacija može biti za 1 do 12 osoba."}), 400

    reservation = {
        "id": next(reservation_ids),
        "name": str(data["name"]).strip(),
        "phone": str(data["phone"]).strip(),
        "date": data["date"],
        "time": str(data["time"]),
        "guests": guests,
        "note": str(data.get("note", "")).strip(),
    }

    try:
        send_reservation_email(reservation)
    except (RuntimeError, OSError, smtplib.SMTPException, ValueError):
        current_app.logger.exception("Slanje e-maila za rezervaciju nije uspelo.")
        return jsonify({
            "error": "Rezervacija trenutno nije poslata. Proverite SMTP podešavanja ili pokušajte ponovo kasnije."
        }), 503

    reservations.append(reservation)
    return jsonify({
        "message": "Zahtev za rezervaciju je poslat restoranu e-mailom. Sačekaćemo da vas kontaktiramo radi potvrde.",
        "reservation": reservation,
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
