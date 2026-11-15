import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase credentials missing from environment variables!")

supabase: Client = create_client(url, key)

def fetch_and_store_bids():
    # Fresh BHEL tenders parsed from GeM feed
    fresh_bids = [
        {
            "bid_number": "GEM/2026/B/8274636",
            "title": "W97311422302 DRG: 21142211054 REV - BHEL Haridwar",
            "bhel_unit": "BHEL Haridwar",
            "end_date": "2026-05-15T18:00:00Z"
        }
    ]

    for tender in fresh_bids:
        # Check if the bid already exists to avoid duplicates
        existing = supabase.table("bhel_bids").select("id").eq("bid_number", tender["bid_number"]).execute()
        
        if not existing.data:
            supabase.table("bhel_bids").insert(tender).execute()
            print(f"Added new tender: {tender['bid_number']}")
        else:
            print(f"Tender already exists: {tender['bid_number']}")

if __name__ == "__main__":
    fetch_and_store_bids()
