
import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials missing!")

url = f"{SUPABASE_URL}/rest/v1/bhel_bids"

headers = {
    "apikey": SUPABASE_KEY
}

try:
    response = requests.get(
        url,
        headers=headers,
        params={"select": "id", "limit": "1"},
        timeout=20
    )

    print("Supabase HTTP status:", response.status_code)

    if response.status_code == 200:
        print("SUCCESS: GitHub connected to Supabase!")
        print("Database table bhel_bids is accessible.")
        print("Response:", response.text)
    else:
        print("Supabase returned an error:")
        print(response.text)
        raise RuntimeError("Supabase connection test failed")

except requests.RequestException as e:
    print("Connection error:", e)
    raise
