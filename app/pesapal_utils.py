
# app/pesapal_utils.py
import base64, uuid, requests
from flask import current_app

PESAPAL_BASE = "https://cybqa.pesapal.com/pesapalv3"

def get_pesapal_token():
    # fetch credentials from config
    creds = f"{current_app.config['PESAPAL_CONSUMER_KEY']}:{current_app.config['PESAPAL_CONSUMER_SECRET']}"
    encoded = base64.b64encode(creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    res = requests.get(f"{PESAPAL_BASE}/api/Auth/RequestToken", headers=headers)
    res.raise_for_status()
    return res.json()["token"]

def register_ipn_url():
    token = get_pesapal_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": "https://your-public-ngrok-url/webhook/pesapal",
        "ipn_notification_type": "POST"
    }

    res = requests.post(f"{PESAPAL_BASE}/api/URLSetup/RegisterIPN", headers=headers, json=payload)
    res.raise_for_status()
    return res.json()  # Save this IPN ID for reuse