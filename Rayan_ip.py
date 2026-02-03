import json
import urllib.request
import os
import sys
import subprocess
import datetime
import time
import random

VERSION = "3.0 Shadow Animated"

class IPLocatorShadow:

    def __init__(self):
        self.colors = [
            '\033[91m',  # Red
            '\033[92m',  # Green
            '\033[93m',  # Yellow
            '\033[94m',  # Blue
            '\033[95m',  # Magenta
            '\033[96m',  # Cyan
        ]
        self.W = '\033[97m'
        self.log_file = "ip_history.txt"

    def clear(self):
        os.system("clear")

    def type_effect(self, text, speed=0.002):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def animated_banner(self):
        self.clear()
        banner = """

██████╗  █████╗ ██╗   ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
██████╔╝███████║ ╚████╔╝ ███████║██╔██╗ ██║
██╔══██╗██╔══██║  ╚██╔╝  ██╔══██║██║╚██╗██║
██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝

⟁ Rayan AlQahtani • Shadow Terminal ⟁
IP Locator Pro Max — Version """ + VERSION + """

System Status : ACTIVE
Initializing Network Intelligence...
"""
        color = random.choice(self.colors)
        self.type_effect(color + banner + self.W, 0.0008)

    def fetch(self, target=""):
        url = f"http://ip-api.com/json/{target}?fields=66846719"
        try:
            response = urllib.request.urlopen(url)
            return json.load(response)
        except:
            print("\033[91m[!] Network Error\033[97m")
            return None

    def save_history(self, data):
        with open(self.log_file, "a") as f:
            f.write(f"\n[{datetime.datetime.now()}]\n")
            for k, v in data.items():
                f.write(f"{k}: {v}\n")
            f.write("-" * 40)

    def copy_clipboard(self, text):
        try:
            subprocess.run(["termux-clipboard-set", text])
            print("\033[92m[✓] IP copied to clipboard\033[97m")
        except:
            print("\033[91m[!] Clipboard failed (Install termux-api)\033[97m")

    def show(self, data):
        if not data or data.get("status") != "success":
            print("\033[91m[!] Invalid IP\033[97m")
            return

        print("\n━━━━━━━━ FULL IP DETAILS ━━━━━━━━\n")

        for k, v in data.items():
            color = random.choice(self.colors)
            print(color + f"{k.capitalize():15}: {v}" + self.W)

        map_link = f"https://www.google.com/maps/place/{data.get('lat')}+{data.get('lon')}"
        print("\nGoogle Maps:", map_link)

        print("\n━━━━━━━━ SECURITY ANALYSIS ━━━━━━━━\n")
        if data.get("proxy"):
            print("\033[91m[!] Proxy/VPN Detected\033[97m")
        else:
            print("\033[92m[✓] No Proxy Detected\033[97m")

        if data.get("hosting"):
            print("\033[93m[!] Hosting/Datacenter IP\033[97m")
        else:
            print("\033[92m[✓] Residential IP Likely\033[97m")

        self.copy_clipboard(data.get("query"))
        self.save_history(data)

    def my_ip(self):
        data = self.fetch("")
        self.show(data)

    def other_ip(self):
        target = input("\033[96mEnter IP or Domain: \033[97m")
        if target.strip():
            data = self.fetch(target)
            self.show(data)

    def view_history(self):
        if not os.path.exists(self.log_file):
            print("\033[91mNo History Found\033[97m")
            return
        with open(self.log_file, "r") as f:
            print("\n━━━━━━━━ HISTORY ━━━━━━━━\n")
            print(f.read())

    def menu(self):
        while True:
            print("""
[1] Quick My IP
[2] Lookup Other IP
[3] View History
[4] Clear Screen
[5] Exit
""")
            choice = input("\033[96mSelect Option: \033[97m")

            if choice == "1":
                self.my_ip()
            elif choice == "2":
                self.other_ip()
            elif choice == "3":
                self.view_history()
            elif choice == "4":
                self.animated_banner()
            elif choice == "5":
                print("\033[92mExiting Shadow Terminal...\033[97m")
                sys.exit()
            else:
                print("\033[91mInvalid Option\033[97m")

    def run(self):
        self.animated_banner()
        self.menu()


if __name__ == "__main__":
    IPLocatorShadow().run()

