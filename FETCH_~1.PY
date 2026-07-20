"""Fetch ~3 months of daily closes for the theme universe and write data.json.

Runs in GitHub Actions (see .github/workflows/update.yml). Uses yfinance - no API key.
"""
import json, datetime
import yfinance as yf

TICKERS = {
    "SMH":  "SEMICONDUCTORS",
    "BOTZ": "ROBOTICS",
    "ROBO": "INDUSTRIAL AUTOMATION",
    "QTUM": "QUANTUM COMPUTING",
    "SNSR": "INTERNET OF THINGS",
    "AIQ":  "ARTIFICIAL INTELLIGENCE",
    "XLK":  "BIG TECH / HARDWARE",
    "IBIT": "CRYPTO / BTC",
    "ICLN": "CLEAN ENERGY",
    "DRIV": "ELECTRIC VEHICLES",
    "REMX": "RARE EARTHS",
    "IYZ":  "TELECOM",
}

MAX_SESSIONS = 63  # ~3 months

def main():
    px = yf.download(
        list(TICKERS), period="5mo", interval="1d",
        auto_adjust=True, progress=False,
    )["Close"]

    series = {}
    for tkr, name in TICKERS.items():
        s = px[tkr].dropna().tail(MAX_SESSIONS)
        if len(s) < 30:
            print(f"WARN: {tkr} only {len(s)} sessions - skipped")
            continue
        series[tkr] = {
            "name": name,
            "dates": [d.strftime("%Y-%m-%d") for d in s.index],
            "closes": [round(float(v), 4) for v in s.values],
        }

    out = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "series": series,
    }
    with open("data.json", "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"Wrote data.json - {len(series)} tickers, "
          f"latest close {max(v['dates'][-1] for v in series.values())}")

if __name__ == "__main__":
    main()
