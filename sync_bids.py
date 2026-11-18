import os
import requests

# Automatically read secrets from GitHub Environment
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

# In a full production scraper, you would fetch official listings from GeM here.
# For now, this template automatically pushes tracked live BHEL tenders on schedule.
tenders_to_sync = [
    {
        "bid_number": "GEM/2026/B/8283875",
        "title": "Partial Discharge Instrument - BHEL Haridwar",
        "bhel_unit": "BHEL Haridwar",
        "end_date": "2026-11-28T18:00:00Z"
    },
    {
        "bid_number": "GEM/2026/B/8281742",
        "title": "SUMP PUMP & MOTOR ASSEMBLY - BHEL Trichy",
        "bhel_unit": "BHEL Trichy",
        "end_date": "2026-11-28T07:30:00Z"
    }
]

print(f"Syncing {len(tenders_to_sync)} BHEL tenders to Supabase...")

for tender in tenders_to_sync:
    response = requests.post(url, headers=headers, json=tender)
    if response.status_code in [200, 201]:
        print(f"Successfully synced: {tender['bid_number']}")
    else:
        print(f"Skipped or error for {tender['bid_number']}: {response.text}")
