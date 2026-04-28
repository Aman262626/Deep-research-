from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://htmlweb.ru/geo/api.php?json&telcod="
NOT_FOUND = "जानकारी उपलब्ध नहीं"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
)


def lookup_number(phone: str) -> dict:
    try:
        resp = requests.get(
            API_URL + phone,
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        if not resp.ok:
            return {"error": "डेटा नहीं मिला"}
        data = resp.json()
    except requests.exceptions.RequestException:
        return {"error": "सर्वर से कनेक्शन में त्रुटि"}

    if data.get("limit", 1) <= 0:
        return {"error": "लिमिट खत्म हो गई"}
    if data.get("error") or data.get("status_error"):
        return {"error": "डेटा नहीं मिला"}

    country = data.get("country", {})
    capital = data.get("capital", {})
    region = data.get("region", {
        "autocod": NOT_FOUND,
        "name": NOT_FOUND,
        "okrug": NOT_FOUND,
    })
    other = data.get("0", {})

    country_name = "यूक्रेन" if country.get("country_code3") == "UKR" else (
        f'{country.get("name", NOT_FOUND)}, {country.get("fullname", NOT_FOUND)}'
    )

    result = {
        "country": country_name,
        "city": other.get("name", NOT_FOUND),
        "postal_code": other.get("post", NOT_FOUND),
        "currency_code": country.get("iso", NOT_FOUND),
        "phone_codes": capital.get("telcod", NOT_FOUND),
        "auto_code": region.get("autocod", NOT_FOUND),
        "operator": f'{other.get("oper", NOT_FOUND)}, {other.get("oper_brand", NOT_FOUND)}, {other.get("def", NOT_FOUND)}',
        "location": f'{country.get("name", NOT_FOUND)}, {region.get("name", NOT_FOUND)}, {other.get("name", NOT_FOUND)}',
        "geo_location": data.get("location", NOT_FOUND),
        "language": f'{country.get("lang", NOT_FOUND).title()}, {country.get("langcod", NOT_FOUND)}',
        "region": f'{region.get("name", NOT_FOUND)}, {region.get("okrug", NOT_FOUND)}',
        "capital": capital.get("name", NOT_FOUND),
        "lat_lon": f'{other.get("latitude", NOT_FOUND)}, {other.get("longitude", NOT_FOUND)}',
        "limit": data.get("limit", NOT_FOUND),
    }

    links = [
        {"name": "Instagram", "url": "https://www.instagram.com/accounts/password/reset"},
        {"name": "WhatsApp", "url": f"https://api.whatsapp.com/send?phone={phone}&text=नमस्ते"},
        {"name": "Facebook", "url": "https://facebook.com/login/identify"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com/checkpoint/rp/request-password-reset"},
        {"name": "OK.ru", "url": "https://ok.ru/dk?st.cmd=anonymRecoveryStartPhoneLink"},
        {"name": "Twitter", "url": "https://twitter.com/account/begin_password_reset"},
        {"name": "Viber", "url": f"viber://add?number={phone}"},
        {"name": "Telegram", "url": f"https://t.me/{phone}"},
    ]

    return {"data": result, "links": links}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/lookup", methods=["POST"])
def api_lookup():
    body = request.get_json(silent=True) or {}
    phone = body.get("phone", "").strip()
    if not phone:
        return jsonify({"error": "फ़ोन नंबर दर्ज करें"}), 400
    return jsonify(lookup_number(phone))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
