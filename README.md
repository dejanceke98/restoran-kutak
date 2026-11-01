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
- `GET /api/drinks` — pića i cene

Frontend očekuje API na `http://localhost:5000`. Drugi API URL može se postaviti kroz `VITE_API_URL` u `.env` fajlu.

## Napomena

Meni, karta pića, adresa i telefon su primeri i mogu se zameniti stvarnim podacima restorana.
