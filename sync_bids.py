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

def fetch_live_gem_bhel_bids():
    # Official GeM public search API/endpoint query for BHEL
    gem_search_url = "https://gem.gov.in/search/results"
    params = {"q": "BHEL", "page": 1}
    
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(gem_search_url, params=params, headers=req_headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            tenders = data.get("hits", []) # Extracts live search hits from GeM
            
            if not tenders:
                print("No tenders returned from GeM search query.")
                return

            print(f"Found {len(tenders)} live tenders from GeM. Syncing to Supabase...")

            for item in tenders:
                tender_data = {
                    "bid_number": item.get("gem_bid_number"),
                    "title": item.get("title", "BHEL Tender Item"),
                    "bhel_unit": item.get("buyer_org", "BHEL Unit"),
                    "end_date": item.get("end_date", "2026-12-31T18:00:00Z")
                }

                if tender_data["bid_number"]:
                    res = requests.post(supabase_api_url, headers=headers, json=tender_data)
                    if res.status_code in [200, 201]:
                        print(f"Synced new live bid: {tender_data['bid_number']}")
        else:
            print(f"GeM portal returned status code: {response.status_code}. (GeM may be blocking direct automated requests).")

    except Exception as e:
        print(f"Error connecting to GeM search: {e}")

if __name__ == "__main__":
    fetch_live_gem_bhel_bids()
