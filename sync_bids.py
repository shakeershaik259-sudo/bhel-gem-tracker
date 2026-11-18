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

def scrape_official_bhel_tenders():
    # Official BHEL public tender listings page
    portal_url = "https://tenders.bhel.com/tenders"
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        print("Fetching live tenders from BHEL portal...")
        response = requests.get(portal_url, headers=req_headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Failed to fetch portal. Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all rows in the official BHEL tender table
        table = soup.find('table')
        if not table:
            print("Could not locate tender table on page.")
            return

        rows = table.find_all('tr')
        synced_count = 0

        for row in rows[1:]: # Skip table header
            cols = row.find_all('td')
            if len(cols) >= 4:
                # Extract text details directly from BHEL's live publication table
                description = cols[1].get_text(strip=True)
                unit = cols[2].get_text(strip=True)
                closing_date_raw = cols[3].get_text(strip=True)
                
                # Extract GeM bid number if present in the text description
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
                    "end_date": "2026-12-31T18:00:00Z" # Default parsing safety or extracted date
                }

                # Push directly to Supabase database
                res = requests.post(supabase_api_url, headers=headers, json=tender_data)
                if res.status_code in [200, 201]:
                    print(f"Synced active tender: {tender_data['bid_number']}")
                    synced_count += 1

        print(f"Successfully scraped and synced {synced_count} live tenders!")

    except Exception as e:
        print(f"Scraping error: {e}")

if __name__ == "__main__":
    scrape_official_bhel_tenders()
