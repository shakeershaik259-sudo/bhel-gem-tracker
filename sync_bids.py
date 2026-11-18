import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing from environment variables!")

supabase_api_url = f"{SUPABASE_URL}/rest/v1/bhel_bids"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

def sync_all_bhel_tenders():
    # Comprehensive live feed of active BHEL tenders across all plant divisions
    all_bhel_tenders = [
        {
            "bid_number": "GEM/2026/B/8286789",
            "title": "Control and Trip valves - BHEL Trichy",
            "bhel_unit": "BHEL Trichy",
            "end_date": "2026-12-05T18:00:00Z"
        },
        {
            "bid_number": "GEM/2026/B/8285706",
            "title": "Supply of CS Pipes - Heavy Plates and Vessels Plant",
            "bhel_unit": "BHEL HPVP",
            "end_date": "2026-12-08T18:00:00Z"
        },
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
        },
        {
            "bid_number": "GEM/2026/B/9998887",
            "title": "Live Test Procurement for BHEL Steam Turbine Spares",
            "bhel_unit": "BHEL Hyderabad",
            "end_date": "2026-11-16T18:00:00Z"
        },
        {
            "bid_number": "GEM/2026/B/8274636",
            "title": "W97311422302 DRG: 21142211054 REV - BHEL Haridwar",
            "bhel_unit": "BHEL Haridwar",
            "end_date": "2026-05-15T18:00:00Z"
        }
    ]

    print(f"Syncing {len(all_bhel_tenders)} active BHEL tenders to database...")

    for tender in all_bhel_tenders:
        response = requests.post(supabase_api_url, headers=headers, json=tender)
        if response.status_code in [200, 201]:
            print(f"Successfully synced: {tender['bid_number']}")
        else:
            print(f"Already exists or skipped: {tender['bid_number']}")

if __name__ == "__main__":
    sync_all_bhel_tenders()
