# Mystery — Phone Number Lookup

A web application for looking up phone number information using public APIs.

## Features
- Phone number information lookup (country, city, operator, location, etc.)
- Links to check the number on social media platforms
- Clean dark-themed UI
- Ready for Render deployment

## Local Setup

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 in your browser.

## Deploy on Render

1. Push this repo to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click **New → Web Service**
4. Connect your GitHub repo (`Deep-research-`)
5. Render will auto-detect the `render.yaml` config
6. Click **Create Web Service**

The app will be live at `https://mystery-phone-lookup.onrender.com` (or your custom name).
