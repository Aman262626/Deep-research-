# Testing: Mystery Phone Lookup Web App

## Overview
Flask web app that looks up phone number info via the public htmlweb.ru API. Dark-themed UI with results display and social media links.

## Local Dev Setup

```bash
pip install -r requirements.txt
python app.py
# App runs at http://localhost:5000
```

No API keys or credentials needed — the app uses a public API.

## Devin Secrets Needed
None — no authentication required.

## Key Files
- `app.py` — Flask backend with `/api/lookup` POST endpoint
- `templates/index.html` — Single-page dark-themed UI
- `requirements.txt` — Flask, requests, gunicorn
- `Procfile` / `render.yaml` — Render deployment config

## Testing Approach

### Primary Flow: Valid Phone Lookup
1. Open `http://localhost:5000`
2. Enter a valid phone number (e.g. `+79999993993`)
3. Click "Поиск" or press Enter
4. Verify results card shows: country, city, operator, coordinates
5. Verify social links section shows 8 platform buttons

### Edge Cases
- **Empty input**: Should be a no-op (JS guard `if (!phone) return`)
- **Invalid input**: The upstream htmlweb.ru API is lenient — it may return partial data instead of errors for garbage input. This is expected API behavior, not an app bug.

### API Testing via curl
```bash
# Valid lookup
curl -s -X POST http://localhost:5000/api/lookup \
  -H "Content-Type: application/json" \
  -d '{"phone":"+79999993993"}'

# Empty phone (should return 400)
curl -s -X POST http://localhost:5000/api/lookup \
  -H "Content-Type: application/json" \
  -d '{"phone":""}'
```

## Render Deployment
1. Push repo to GitHub
2. Render Dashboard → New → Web Service → connect repo
3. Render auto-detects `render.yaml` config
4. Uses gunicorn as production WSGI server

## Notes
- The htmlweb.ru API has rate limits (shown as "Оставшиеся лимиты" in the UI). If limits are exhausted, the app shows a limit error.
- The API might be slow sometimes (~2-5 seconds). The UI shows a "Поиск данных..." spinner during loading.
- Port 5000 may conflict with other services. Kill existing processes on the port before starting: `fuser -k 5000/tcp`
