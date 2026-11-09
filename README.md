<<<<<<< HEAD
# Phone Intel

Look up the country, region, carrier, line type, time zones and map location of a phone number.
Python (FastAPI) backend, Next.js + Tailwind frontend.

<!-- Add a screenshot here: ![Phone Intel](docs/screenshot.png) -->
**Live demo:** _add your Vercel link_ · **API docs:** _your-api-url_/docs

## Features
- Validation and formatting (E.164, international, national)
- Country, region, carrier, line type and time zones via `phonenumbers`
- Geocoding with OpenCage (cached) and an embedded OpenStreetMap view
- Typed JSON API with auto-generated docs, tests and CI
- CLI version of the original script

## Run it (Windows PowerShell)
```powershell
# backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env        # then put your OpenCage key in .env
uvicorn app.main:app --reload

# frontend (new terminal)
cd frontend
copy .env.example .env.local
npm install
npm run dev
```
Open http://localhost:3000. Or run both with `docker compose up --build`.

## CLI
```powershell
cd backend
pip install folium
python cli.py +27821234567 --map
```

## Tests
```powershell
cd backend; pytest -q
```

## API
`GET /api/lookup?number=+27821234567` or `?number=0821234567&region=ZA`. Full docs at `/docs`.

## Deploy
Frontend on Vercel (root `frontend`, set `NEXT_PUBLIC_API_URL`). Backend on Render or Railway
(root `backend`, start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, set `OPENCAGE_KEY` and `CORS_ORIGINS`).

## Notes
Uses public numbering-plan metadata only. Location is the region the number was issued in, not where the phone is now.
Carrier data reflects the original allocation and may be wrong for ported numbers.

## Roadmap
CSV batch lookup, lookup history in SQLite, rate limiting.
=======
# Phone-Number-Intelligence-Tool
A phone number intelligence tool designed to analyse phone number information, validate number formats and present relevant lookup results.
>>>>>>> f3dc76b390296b2ff6dd1e2d6c9af4f08d18e193
