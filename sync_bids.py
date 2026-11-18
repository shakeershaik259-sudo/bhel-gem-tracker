import os
import requests
from bs4 import BeautifulSoup

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

def sync_bhel_portal_tenders():
    url = "https://tenders.bhel.com/tenders"
    req_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=req_headers, timeout=15)
        if response.status_code != 200:
            print(f"Portal returned status: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            print("Tender table not found.")
            return

        rows = table.find_all('tr')
        synced_count = 0

        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                description = cols[1].get_text(strip=True)
                unit = cols[2].get_text(strip=True)
                
                bid_number = "BHEL-TENDER"
                if "GEM/" in description:
                    parts = description.split("GEM/")
                    for p in parts:
                        if len(p) >= 15:
                            bid_number = "GEM/" + p.split()[0].replace(")", "").replace(";", "")
                            break

                tender_data = {
                    "bid_number": bid_number[:50],
                    "title": description[:250],
                    "bhel_unit": unit[:100] if unit else "BHEL Unit",
                    "end_date": "2026-12-31T18:00:00Z"
                }

                res = requests.post(supabase_api_url, headers=headers, json=tender_data)
                if res.status_code in [200, 201]:
                    print(f"Synced: {tender_data['bid_number']}")
                    synced_count += 1

        print(f"Successfully synced {synced_count} active tenders from BHEL portal.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_bhel_portal_tenders()
