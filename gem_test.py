
import urllib.request

sites = [
    "https://bidplus.gem.gov.in/all-bids",
    "https://www.google.com"
]

for url in sites:
    print("\nTesting:", url)
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            print("Connected:", response.status)
    except Exception as e:
        print("Connection failed:", e)
