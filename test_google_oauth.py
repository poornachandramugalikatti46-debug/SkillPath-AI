import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("GOOGLE_CLIENT_ID")
if not client_id:
    # Try reading frontend/.env as fallback
    try:
        with open("frontend/.env", "r") as f:
            for line in f:
                if line.startswith("VITE_GOOGLE_CLIENT_ID="):
                    client_id = line.split("=", 1)[1].strip()
    except Exception:
        pass

if not client_id:
    print("❌ No GOOGLE_CLIENT_ID found in .env or frontend/.env")
    exit(1)

print(f"Testing Google OAuth Client ID: {client_id}\n")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

all_ok = True
for origin in origins:
    url = f"https://accounts.google.com/gsi/button?client_id={client_id}"
    try:
        res = requests.get(
            url,
            headers={
                "Referer": f"{origin}/",
                "Origin": origin,
            },
            timeout=5,
        )
        if res.status_code == 200:
            print(f"  [PASS] {origin:25} -> ALLOWED (HTTP 200)")
        elif res.status_code == 403:
            all_ok = False
            print(f"  [FAIL] {origin:25} -> NOT ALLOWED (HTTP 403: Origin not in Google Console)")
        else:
            all_ok = False
            print(f"  [WARN] {origin:25} -> HTTP {res.status_code}")
    except Exception as exc:
        all_ok = False
        print(f"  [ERR]  {origin:25} -> Error: {exc}")

print("\n" + "=" * 60)
if all_ok:
    print("SUCCESS: All origins are authorized! Google Sign-In is ready to use.")
else:
    print("ACTION REQUIRED:")
    print("1. Open: https://console.cloud.google.com/apis/credentials")
    print("2. Click your OAuth 2.0 Web Client ID")
    print("3. Under 'Authorized JavaScript origins', add:")
    print("     http://localhost:5173")
    print("     http://127.0.0.1:5173")
    print("4. Click 'SAVE' and wait 2-5 minutes.")
print("=" * 60)
