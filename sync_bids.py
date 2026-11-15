import os
from supabase import create_client, Client

# Debug: Print what keys are available in the environment (safe, doesn't print values)
print("Checking environment variables...")
print(f"SUPABASE_URL exists: {bool(os.environ.get('SUPABASE_URL'))}")
print(f"SUPABASE_KEY exists: {bool(os.environ.get('SUPABASE_KEY'))}")
print(f"SUPABASE_ANON_KEY exists: {bool(os.environ.get('SUPABASE_ANON_KEY'))}")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    raise ValueError("Supabase credentials are still missing in GitHub Actions! Check Step 2 below.")

supabase: Client = create_client(url, key)

def fetch_and_store_bids():
    fresh_bids = [
        {
            "bid_number": "GEM/2026/B/8274636",
            "title": "W97311422302 DRG: 21142211054 REV - BHEL Haridwar",
            "bhel_unit": "BHEL Haridwar",
            "end_date": "2026-05-15T18:00:00Z"
        }
    ]

    for tender in fresh_bids:
        existing = supabase.table("bhel_bids").select("id").eq("bid_number", tender["bid_number"]).execute()
        
        if not existing.data:
            supabase.table("bhel_bids").insert(tender).execute()
            print(f"Added new tender: {tender['bid_number']}")
        else:
            print(f"Tender already exists: {tender['bid_number']}")

if __name__ == "__main__":
    fetch_and_store_bids()
