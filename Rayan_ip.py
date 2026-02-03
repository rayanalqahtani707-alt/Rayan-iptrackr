#!/usr/bin/env python3
import requests
import os
import time
import json
import socket
from datetime import datetime

HISTORY_FILE = "ip_history.json"

colors = ["\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[95m"]
RESET = "\033[0m"

def type_print(text, delay=0.005):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def banner():
    os.system("clear")
    color = colors[int(time.time()) % len(colors)]
    print(color + """
██████╗  █████╗ ██╗   ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
██████╔╝███████║ ╚████╔╝ ███████║██╔██╗ ██║
██╔══██╗██╔══██║  ╚██╔╝  ██╔══██║██║╚██╗██║
██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
        ⟁ Rayan IP Shadow v4 ⟁
""" + RESET)

def save_history(data):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    history.append(data)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def generate_report(data):
    filename = f"IP_Report_{data.get('IP')}.txt"
    with open(filename, "w") as f:
        f.write("=== Rayan IP Shadow Report ===\n\n")
        for k, v in data.items():
            f.write(f"{k}: {v}\n")
    print(f"\n📄 Report saved as {filename}")

def copy_clipboard(text):
    os.system(f'echo "{text}" | termux-clipboard-set')
    print("📋 Copied to clipboard!")

def get_ip_data(ip):
    try:
        r = requests.get(f"https://ipwho.is/{ip}", timeout=5)
        data = r.json()
        if data.get("success"):
            return data
    except:
        pass

    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        return r.json()
    except:
        return None

def display(data):
    if not data:
        print("❌ Failed to fetch data")
        return

    lat = data.get("latitude")
    lon = data.get("longitude")

    if not lat and data.get("loc"):
        loc_split = data.get("loc").split(",")
        lat = float(loc_split[0])
        lon = float(loc_split[1])

    if lat and lon:
        lat = round(float(lat), 6)
        lon = round(float(lon), 6)
        google_map = f"https://www.google.com/maps?q={lat},{lon}"
    else:
        google_map = None

    fields = {
        "IP": data.get("ip"),
        "IP Version": data.get("type"),
        "Continent": data.get("continent"),
        "Country": data.get("country"),
        "Region": data.get("region"),
        "City": data.get("city"),
        "Postal": data.get("postal"),
        "Latitude": lat,
        "Longitude": lon,
        "Timezone": str(data.get("timezone")),
        "ISP": data.get("isp"),
        "Organization": data.get("org"),
        "ASN": data.get("asn"),
        "Currency": str(data.get("currency")),
        "Connection Type": data.get("connection", {}).get("type") if isinstance(data.get("connection"), dict) else None,
        "Proxy/VPN": data.get("proxy"),
        "Hosting": data.get("hosting"),
        "Google Maps": google_map
    }

    print("\n" + "="*60)
    for key, value in fields.items():
        if value:
            print(f"{key}: {value}")
    print("="*60)

    save_history(fields)

    while True:
        print("""
[1] Copy IP
[2] Copy Google Maps Link
[3] Open Google Maps
[4] Generate Shareable Report
[5] Back to Menu
""")
        choice = input("Select: ")

        if choice == "1":
            copy_clipboard(fields.get("IP"))

        elif choice == "2" and google_map:
            copy_clipboard(google_map)

        elif choice == "3" and google_map:
            os.system(f"termux-open '{google_map}'")

        elif choice == "4":
            generate_report(fields)

        elif choice == "5":
            break

        else:
            print("Invalid option")

def main():
    while True:
        banner()
        print("""
[1] Quick My IP
[2] Lookup Other IP
[3] Exit
""")
        choice = input("Select Option: ")

        if choice == "1":
            data = get_ip_data("")
            display(data)

        elif choice == "2":
            ip = input("Enter IP or Domain: ")
            try:
                ip = socket.gethostbyname(ip)
            except:
                pass
            data = get_ip_data(ip)
            display(data)

        elif choice == "3":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option")
            time.sleep(1)

if __name__ == "__main__":
    main()
