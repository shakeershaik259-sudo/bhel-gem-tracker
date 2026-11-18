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

def fetch_all_gem_bhel_tenders():
    # GeM public search API endpoint for BHEL
    gem_url = "https://gem.gov.in/search/results"
    
    # We loop through pages to grab all available live BHEL listings
    page = 1
    total_synced = 0

    while page <= 3: # Scans up to the first 3 pages of active results
        params = {"q": "BHEL", "page": page}
        req_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest"
        }

        try:
            print(f"Fetching GeM BHEL tenders - Page {page}...")
            response = requests.get(gem_url, params=params, headers=req_headers, timeout=15)
            
            if response.status_code != 200:
                print(f"GeM portal responded with status code: {response.status_code}")
                break

            data = response.json()
            tenders = data.get("hits", [])

            if not tenders:
                print("No more tenders found on GeM search.")
                break

            for item in tenders:
                tender_data = {
                    "bid_number": item.get("gem_bid_number"),
                    "title": item.get("title", "BHEL Tender"),
                    "bhel_unit": item.get("buyer_org", "BHEL Unit"),
                    "end_date": item.get("end_date", "2026-12-31T18:00:00Z")
                }

                if tender_data["bid_number"]:
                    res = requests.post(supabase_api_url, headers=headers, json=tender_data)
                    if res.status_code in [200, 201]:
                        print(f"Synced live GeM bid: {tender_data['bid_number']}")
                        total_synced += 1

            page += 1
        except Exception as e:
            print(f"Error fetching from GeM: {e}")
            break

    print(f"Finished! Successfully synced {total_synced} live BHEL tenders from GeM.")

if __name__ == "__main__":
    fetch_all_gem_bhel_tenders()
