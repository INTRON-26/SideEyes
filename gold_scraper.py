import requests
import datetime
import time
import json
import signal
import sys
import atexit

URL = "https://statewisebcast.dpgold.in:7768/VOTSBroadcastStreaming/Services/xml/GetLiveRateByTemplateID/dpgold"

rates = []


def fetch_gold_rates():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }

    r = requests.get(URL, headers=headers, timeout=10)
    r.raise_for_status()

    lines = r.text.strip().split("\n")

    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 5 and parts[2] == "GOLD Andhra Pradesh - Telangana 999":
            return {
                "time": datetime.datetime.now().isoformat(),
                "price": parts[4]
            }

    return None


def save_results(filename="scraped_gold_data.json"):
    if not rates:
        print("No data to save.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(rates, f, indent=2)

    print(f"Saved {len(rates)} records to {filename}")


atexit.register(save_results)


def handle_exit(signal_number, frame):
    print("\nStopping scraper...")
    save_results()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # kill


if __name__ == "__main__":
    print("Starting gold rate scraper. Press Ctrl+C to stop.")

    while True:
        rate = fetch_gold_rates()
        if rate:
            rates.append(rate)
            print(rate)

        time.sleep(1800)
