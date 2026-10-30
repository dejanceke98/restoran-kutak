# Kutak — mali restoran

Responsive sajt na srpskom za restoran Kutak. Frontend je Vue 3 + Vite + Bootstrap 5, a backend je Flask JSON API.

## Potrebno

- Node.js 20.19+ ili 22.12+
- Python 3.10+

## Pokretanje u Windows PowerShell-u

### 1. Flask API

Iz glavnog direktorijuma projekta:

```powershell
py -m venv backend\.venv
.\backend\.venv\Scripts\Activate.ps1
py -m pip install -r backend\requirements.txt
py backend\app.py
```

Flask API radi na `http://localhost:5000`. Ako PowerShell blokira aktivaciju okruženja, pokrenite komande instalacije koristeći `backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt`, pa API pokrenite sa `backend\.venv\Scripts\python.exe backend\app.py`.

### 2. Vue frontend

Otvorite drugi PowerShell terminal u glavnom direktorijumu projekta:

```powershell
npm install
npm run dev
```

Otvorite adresu koju Vite ispiše u terminalu (podrazumevano `http://localhost:5173`). Za izgradnju produkcijske verzije pokrenite `npm run build`.

## API rute

- `GET /api/health` — provera dostupnosti API-ja
- `GET /api/menu` — jela i cene
- `POST /api/reservations` — validacija i prijem rezervacije

Frontend očekuje API na `http://localhost:5000`. Drugi API URL može se postaviti kroz `VITE_API_URL` u `.env` fajlu.

## Slanje rezervacija e-mailom

Flask šalje e-mail restoranu pre nego što potvrdi prijem rezervacije. SMTP parametre postavite u `.env` fajlu u glavnom direktorijumu projekta (primer je u `.env.example`). Nemojte deliti niti commit-ovati `.env` fajl; lozinku čuvajte kao tajnu.

Primer za Gmail: uključite verifikaciju u 2 koraka na Google nalogu i koristite Google App Password kao `SMTP_PASSWORD` (ne običnu lozinku naloga). Za druge provajdere unesite njihove SMTP podatke.

Posle promene `.env` fajla restartujte Flask. Ako SMTP podešavanja nedostaju ili slanje ne uspe, API vraća grešku i rezervacija se ne potvrđuje kao poslata.

## Napomena

Rezervacije se trenutno čuvaju samo u memoriji procesa Flask-a. Podaci se brišu kada se server restartuje; ovo je demonstraciona implementacija, nije trajna produkcijska evidencija. Adresa, telefon i meni su primeri i mogu se zameniti stvarnim podacima restorana.
