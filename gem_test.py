
import urllib.request

url = "https://bidplus.gem.gov.in/advance-search"

try:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        print("Status:", response.status)
        print("Page URL:", response.url)
        html = response.read().decode("utf-8", errors="replace")
        print("Page length:", len(html))
        print("HTML received successfully.")
except Exception as e:
    print("Test failed:", e)
