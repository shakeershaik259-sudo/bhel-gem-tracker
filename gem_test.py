
import json
import re
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from http.cookiejar import CookieJar
from urllib.request import HTTPCookieProcessor

BASE = "https://bidplus.gem.gov.in"
opener = build_opener(HTTPCookieProcessor(CookieJar()))
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}

try:
    html = opener.open(BASE + "/all-bids", timeout=20).read().decode("utf-8", errors="replace")
    match = re.search(r"csrf_bd_gem_nk.*?'([a-f0-9]{32})'", html)

    if not match:
        print("Could not obtain the public-page token. Test stopped.")
        raise SystemExit

    csrf = match.group(1)

    payload = {
        "page": 1,
        "param": {"searchBid": "BHEL", "searchType": "fullText"},
        "filter": {
            "bidStatusType": "ongoing_bids",
            "byType": "all",
            "highBidValue": "",
            "byEndDate": {"from": "", "to": ""},
            "sort": "Bid-End-Date-Latest"
        }
    }

    body = urlencode({
        "payload": json.dumps(payload, separators=(",", ":")),
        "csrf_bd_gem_nk": csrf
    }).encode()

    request_headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Referer": BASE + "/all-bids",
        "Origin": BASE,
        "X-Requested-With": "XMLHttpRequest"
    }

    req = Request(BASE + "/all-bids-data", data=body, headers=request_headers)
    response = opener.open(req, timeout=20).read().decode("utf-8")
    data = json.loads(response)

    print("GeM response code:", data.get("code"))
    response_data = data.get("response", {}).get("response", {})
    print("Total matching results:", response_data.get("numFound", 0))

    docs = response_data.get("docs", [])
    for i, doc in enumerate(docs[:10], 1):
        print("\n--- BID", i, "---")
        for key in [
            "b_bid_number",
            "bbt_title",
            "ba_official_details_deptName",
            "ba_official_details_minName",
            "ba_official_details_orgName",
            "b_id"
        ]:
            print(key + ":", doc.get(key))

except Exception as e:
    print("Test failed:", str(e))
