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
import argparse

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
 {Fore.BLUE}███████ ██      ██      ███████  ██████ ██   ██ ██     ██ ██   ████ ██████  ██   ██  
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

def scan_ports(ip, start_port, direction="up", max_port=65535, step=20, delay=1, fail_limit=4, skip_ports_val=250):
    scanner = nmap.PortScanner()
    scanned_ports = []
    skip_ports = 0
    fail_counter = 0
    port = start_port
    server_count = 0
    reversed_once = False 

    #create folder for serwer results
    results_dir = "Results"
    os.makedirs(results_dir, exist_ok=True)

    #generate filename with date and time
    now = datetime.datetime.now()
    filename = os.path.join(results_dir, now.strftime("%Y-%m-%d_%H-%M-%S") + "servers.txt")

    def next_port(p, skip=0, dirn=direction):
        if dirn == "down":
            return max(p - step - skip, 1)
        else:
            return min(p + step + skip, max_port)

    try:
        with open(filename, "w", encoding="utf-8") as output_file:
            while True:
                #if reach the bootom or top of the range 
                if direction == "up" and port > max_port and not reversed_once:
                    direction = "down"
                    port = start_port
                    reversed_once = True
                    print(f"{Fore.LIGHTYELLOW_EX}Reached the top. Reversing direction to DOWN from port {start_port}.{Style.RESET_ALL}")
                    continue
                elif direction == "down" and port < 1 and not reversed_once:
                    direction = "up"
                    port = start_port
                    reversed_once = True
                    print(f"{Fore.LIGHTYELLOW_EX}Reached the bottom. Reversing direction to UP from port {start_port}.{Style.RESET_ALL}")
                    continue
                elif reversed_once and ((direction == "up" and port > max_port) or (direction == "down" and port < 1)):
                    break  #end the scan if we reach the limits again

                if skip_ports > 0:
                    port = next_port(port, skip_ports, direction)
                    skip_ports = 0

                if direction == "up":
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
                                        server_count += 1
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
                    if fail_counter >= fail_limit:
                        print(f"{Fore.WHITE}No servers found in {fail_limit} consecutive scans. Skipping {skip_ports_val} ports...{Style.RESET_ALL}")
                        skip_ports = skip_ports_val
                        fail_counter = 0

                port = next_port(port, dirn=direction)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Minecraft Server Port Scanner by @ganduspl",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-a", "--address", type=str, help="IP address with port, e.g. 1.2.3.4:25565")
    parser.add_argument("-d", "--direction", choices=["u", "d"], default="u", help="Scan direction: up (u) or down (d)")
    parser.add_argument("--fail-limit", type=int, default=4, help="How many fails before skipping")
    parser.add_argument("--skip-ports", type=int, default=250, help="How many ports to skip after fails")
    parser.add_argument("--step", type=int, default=20, help="Step size for port scanning")
    parser.add_argument("--delay", type=float, default=1, help="Delay between scans (seconds)")
    parser.add_argument("--max-port", type=int, default=65535, help="Maximum port to scan")

    args = parser.parse_args()

    if args.address:
        if ':' not in args.address:
            print("Invalid format. Required format is IP:PORT.")
            exit()
        ip, port_str = args.address.split(':')
        try:
            start_port = int(port_str)
        except ValueError:
            print("Port must be an integer.")
            exit()
        direction = "up" if args.direction == "u" else "down"
        scan_ports(
            ip, start_port,
            direction=direction,
            max_port=args.max_port,
            step=args.step,
            delay=args.delay,
            fail_limit=args.fail_limit,
            skip_ports_val=args.skip_ports
        )
    else:
        # =====================
        # all inputs for starts
        # =====================
        address = input(f"{Fore.WHITE}Enter IP address with port {Fore.BLUE}( {Fore.LIGHTCYAN_EX}e.g. 0.0.0.0:25557{Fore.BLUE} ){Fore.WHITE} : ")
        if ':' not in address:
            print("Invalid format. Required format is IP:PORT.")
            exit()

        ip, port_str = address.split(':')
        try:
            start_port = int(port_str)
        except ValueError:
            print("Port must be an integer.")
            exit()

        direction_input = input(f"{Fore.WHITE}Scan up (+25) or down (-25)? {Fore.BLUE}( {Fore.LIGHTCYAN_EX}u/d default: u{Fore.BLUE} ) {Fore.WHITE}: ").strip().lower()
        if direction_input not in ["u", "d", ""]:
            print(f"{Fore.WHITE}Invalid choice. Use 'u', 'd' or leave empty for default (up).")
            exit()
        direction = "up" if direction_input in ["u", ""] else "down"

        fail_limit_input = input(f"{Fore.WHITE}How many fails before skipping? {Fore.BLUE}( {Fore.LIGHTCYAN_EX}default: 4{Fore.BLUE} ) {Fore.WHITE}: ").strip()
        skip_ports_input = input(f"{Fore.WHITE}How many ports to skip after fails? {Fore.BLUE}( {Fore.LIGHTCYAN_EX}default: 250{Fore.BLUE} ) {Fore.WHITE}: ").strip()
        try:
            fail_limit = int(fail_limit_input) if fail_limit_input else 4
        except ValueError:
            fail_limit = 4
        try:
            skip_ports_val = int(skip_ports_input) if skip_ports_input else 250
        except ValueError:
            skip_ports_val = 250

        scan_ports(ip, start_port, direction=direction, fail_limit=fail_limit, skip_ports_val=skip_ports_val)
