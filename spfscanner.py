import nmap
import time
import re
import socket
import struct
from mcstatus import JavaServer
from colorama import init, Fore, Style
import requests
import json
import datetime
import os

# =====================
# script made by @ganduspl
#
# feel free to use and modify it :D
# it can be used for educational purposes
# =====================

init(autoreset=True)
init()

#minecraf color codes map
MC_COLOR_MAP = {
    '0': Fore.BLACK,
    '1': Fore.BLUE,
    '2': Fore.GREEN,
    '3': Fore.CYAN,
    '4': Fore.RED,
    '5': Fore.MAGENTA,
    '6': Fore.YELLOW,
    '7': Fore.WHITE,
    '8': Fore.LIGHTBLACK_EX,
    '9': Fore.LIGHTBLUE_EX,
    'a': Fore.LIGHTGREEN_EX,
    'b': Fore.LIGHTCYAN_EX,
    'c': Fore.LIGHTRED_EX,
    'd': Fore.LIGHTMAGENTA_EX,
    'e': Fore.LIGHTYELLOW_EX,
    'f': Fore.LIGHTWHITE_EX,
    'r': Style.RESET_ALL,
    'l': Style.BRIGHT,
    'n': '',  #no in colorama
    'o': '', # no in colorama
    'm': '',  #  no in colorama
}
ascii_art = f"""{Fore.LIGHTCYAN_EX}
 ███████ ██████  ███████ ███████  ██████  █████  ███    ██ ███    ██ ███████ ██████  
 ██      ██   ██ ██      ██      ██      ██   ██ ████   ██ ████   ██ ██      ██   ██ 
 {Fore.CYAN}███████ ██████  █████   ███████ ██      ███████ ██ ██  ██ ██ ██  ██ █████   ██████  
     {Fore.LIGHTBLUE_EX} ██ ██      ██           ██ ██      ██   ██ ██  ██ ██ ██  ██ ██ ██      ██   ██ 
 {Fore.BLUE}███████ ██      ██      ███████  ██████ ██   ██ ██   ██ ██   ████ ██   ████ ███████ ██   ██  
{Style.RESET_ALL}"""

title = f"{Fore.LIGHTCYAN_EX}Server{Fore.CYAN}Port{Fore.LIGHTBLUE_EX}Finder {Fore.WHITE}Minecraft Scanner{Style.RESET_ALL}"
author = f"{Fore.WHITE}( by {Fore.LIGHTCYAN_EX}@ganduspl{Fore.WHITE} ){Style.RESET_ALL}"

print(ascii_art)
print(f"\n                   {title}")
print(f"                        {author}\n")

def minecraft_color_to_colorama(text):
    #deletes minecraft new rbg colors codes ;D
    text = re.sub(r'§#[0-9A-Fa-f]{6}', '', text)
    return re.sub(r'§([0-9a-frlonmk])', lambda m: MC_COLOR_MAP.get(m.group(1).lower(), ''), text) + Style.RESET_ALL

def strip_minecraft_colors(text):
    #delates all minecraft colors codse for txt file
    text = re.sub(r'§#[0-9A-Fa-f]{6}', '', text)
    return re.sub(r'§[0-9a-frlonmk]', '', text, flags=re.IGNORECASE)

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def mc_api_status(ip, port):
    try:
        url = f"https://api.mcsrvstat.us/2/{ip}:{port}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("online"):
                motd_raw = data.get("motd", {}).get("raw", [""])[0]
                motd_clean = data.get("motd", {}).get("clean", [""])[0]
                motd_colored = minecraft_color_to_colorama(motd_raw)
                version = data.get("version", "")
                players = data.get("players", {})
                online = players.get("online", 0)
                maxp = players.get("max", 0)
                return motd_colored, motd_clean, f"{Fore.LIGHTCYAN_EX}Version: {version} {Fore.WHITE}| Players: {Fore.LIGHTCYAN_EX}{online}{Fore.WHITE}/{Fore.LIGHTBLUE_EX}{maxp}"
            else:
                return None, None, None
        else:
            return None, None, None
    except Exception:
        return None, None, None

def scan_ports(ip, start_port, direction="down", max_port=65535, step=25, delay=1):
    scanner = nmap.PortScanner()
    scanned_ports = []
    skip_ports = 0
    fail_counter = 0
    port = start_port
    server_count = 0

    #create folder for serwer results
    results_dir = "Results"
    os.makedirs(results_dir, exist_ok=True)

    #generate filename with date and time
    now = datetime.datetime.now()
    filename = os.path.join(results_dir, now.strftime("%Y-%m-%d_%H-%M-%S") + "servers.txt")

    def next_port(p, skip=0):
        if direction == "down":
            return min(p + step + skip, max_port)
        else:
            return max(p - step - skip, 1)

    try:
        with open(filename, "w", encoding="utf-8") as output_file:
            while (port <= max_port and direction == "down") or (port > 0 and direction != "down"):
                if skip_ports > 0:
                    port = next_port(port, skip_ports)
                    skip_ports = 0

                if direction == "down":
                    end_port = min(port + step - 1, max_port)
                else:
                    end_port = max(port - step + 1, 1)

                port_range = f"{min(port, end_port)}-{max(port, end_port)}"
                print(f"\n{Fore.WHITE}Scanning {Fore.LIGHTCYAN_EX}{ip}{Fore.WHITE}:{Fore.LIGHTCYAN_EX}{port_range}{Style.RESET_ALL}...")

                found_server = False
                try:
                    scanner.scan(hosts=ip, ports=port_range, arguments='-T4')
                    for host in scanner.all_hosts():
                        for proto in scanner[host].all_protocols():
                            ports = scanner[host][proto].keys()
                            for p in sorted(ports):
                                state = scanner[host][proto][p]['state']
                                if state == 'open':
                                    motd_colored, motd_clean, info = mc_api_status(ip, p)
                                    if motd_colored:
                                        found_server = True
                                        server_count += 1  #counting serers thats work
                                        print(f"{Fore.WHITE}Server detected: {Fore.LIGHTCYAN_EX}{ip}:{p}{Fore.WHITE} | {motd_colored} {Fore.WHITE}|{Fore.WHITE} {info}{Style.RESET_ALL}")
                                        output_file.write(f"{ip}:{p} | {motd_clean} | {strip_ansi(info)}\n")
                                    else:
                                        print(f"{Fore.WHITE}Open port (not Minecraft or no response): {Fore.LIGHTCYAN_EX}{ip}:{p}{Style.RESET_ALL}")
                                        output_file.write(f"{ip}:{p} | Open port (not Minecraft or no response)\n")
                except Exception as e:
                    print(f"{Fore.WHITE}Error while scanning {Fore.LIGHTCYAN_EX}{ip}:{port_range}{Fore.WHITE}: {e}{Style.RESET_ALL}")

                if found_server:
                    fail_counter = 0
                else:
                    fail_counter += 1
                    if fail_counter >= 3:
                        print(f"{Fore.WHITE}No servers found in 3 consecutive scans. Skipping 500 ports...{Style.RESET_ALL}")
                        skip_ports = 500
                        fail_counter = 0

                port = next_port(port)
                time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{Fore.LIGHTRED_EX}Scan interrupted by user (Ctrl+C). Saving results...{Style.RESET_ALL}")

    #if scan end Ctrl+C saving results to txt
    new_filename = os.path.join(
        results_dir,
        now.strftime("%Y-%m-%d_%H-%M-%S") + f"_found{server_count}_servers.txt"
    )
    os.rename(filename, new_filename)
    print(f"\n{Fore.LIGHTCYAN_EX}Results saved to: {Fore.WHITE}{new_filename}{Style.RESET_ALL}")

# =====================
# all inputs for starts
# =====================
address = input(f"Enter IP address with port {Fore.BLUE}( {Fore.LIGHTCYAN_EX}e.g. 0.0.0.0:25557{Fore.BLUE} ){Style.RESET_ALL} : ")
if ':' not in address:
    print("Invalid format. Required format is IP:PORT.")
    exit()

ip, port_str = address.split(':')
try:
    start_port = int(port_str)
except ValueError:
    print("Port must be an integer.")
    exit()

#scanning direction ;o
direction_input = input("Scan up (+25) or down (-25)? (u/d): ").strip().lower()
if direction_input not in ["u", "d"]:
    print("Invalid choice. Use 'u' or 'd'.")
    exit()

scan_ports(ip, start_port, direction="down" if direction_input == "d" else "up")
