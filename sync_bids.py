import requests

# Put your actual Supabase URL and Anon Key right here
SUPABASE_URL = "https://rppgxoqqvyzmiewzkpxa.supabase.co"
SUPABASE_KEY = "sb_publishable_WjccgngW8-r7gilAJR3YCg_R5STrIZT"

url = f"{SUPABASE_URL}/rest/v1/bhel_bids"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

tender = {
    "bid_number": "GEM/2026/B/8274636",
    "title": "W97311422302 DRG: 21142211054 REV - BHEL Haridwar",
    "bhel_unit": "BHEL Haridwar",
    "end_date": "2026-05-15T18:00:00Z"
}

print("Sending tender to Supabase via REST API...")
response = requests.post(url, headers=headers, json=tender)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code in [200, 201]:
    print("Success! Tender added.")
else:
    raise Exception(f"Failed to insert tender: {response.text}")
