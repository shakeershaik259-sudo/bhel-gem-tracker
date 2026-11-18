import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing from environment variables!")

url = f"{SUPABASE_URL}/rest/v1/bhel_bids"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

tender = {
    "bid_number": "GEM/2026/B/8283875",
    "title": "Partial Discharge Instrument - BHEL Haridwar",
    "bhel_unit": "BHEL Haridwar",
    "end_date": "2026-11-28T18:00:00Z"
}

print(f"Connecting to Supabase at: {SUPABASE_URL}")

try:
    response = requests.post(url, headers=headers, json=tender, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code in [200, 201]:
        print("Successfully synced tender!")
    else:
        raise Exception(f"Supabase rejected request: {response.text}")
except requests.exceptions.Timeout:
    print("Error: Connection to Supabase timed out. Check if your SUPABASE_URL is correct.")
    raise
