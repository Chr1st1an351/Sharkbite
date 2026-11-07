import os
import time
import socket
import sys
import subprocess
from datetime import datetime

os.system("clear")

print("\033[38;5;51m              ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗██████╗ ██╗████████╗███████╗\033[0m")
time.sleep(0.09)
print("\033[38;5;51m              ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║╚══██╔══╝██╔════╝\033[0m")
time.sleep(0.09)
print("\033[38;5;51m              ███████╗███████║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║   █████╗\033[0m")
time.sleep(0.09)
print("\033[38;5;51m              ╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║   ██╔══╝\033[0m")
time.sleep(0.09)
print("\033[38;5;51m              ███████║██║  ██║██║  ██║██║  ██║██║  ██╗██████╔╝██║   ██║   ███████╗\033[0m")
time.sleep(0.09)
print("\033[38;5;51m              ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝\033[0m")
time.sleep(0.09)

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def get_target():
    """Helper function to prompt and validate a target host."""
    host = input(f"\n{Colors.BOLD}Enter target domain or IP (e.g., 127.0.0.1): {Colors.ENDC}").strip()
    if not host:
        print(f"{Colors.FAIL}[!] Error: Target cannot be blank.{Colors.ENDC}")
        return None
    try:
        target_ip = socket.gethostbyname(host)
        print(f"{Colors.GREEN}[+] Target resolved successfully -> {target_ip}{Colors.ENDC}")
        return target_ip
    except socket.gaierror:
        print(f"{Colors.FAIL}[!] Error: Could not resolve hostname '{host}'{Colors.ENDC}")
        return None

def grab_banner(ip, port):
    """Attempts to grab a service banner from an open port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((ip, port))
        try:
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        except:
            pass
        banner_data = s.recv(1024)
        s.close()
        return banner_data.decode(errors='ignore').strip()
    except Exception:
        return None

def quick_scan(target_ip):
    """Scans a hardcoded list of the most common ports."""
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 8080, 8443]
    print(f"\n{Colors.BLUE}[*] Running Quick Scan on {len(common_ports)} common ports...{Colors.ENDC}")
    run_scan(target_ip, common_ports)

def custom_scan(target_ip):
    """Allows the user to specify manual ports to check."""
    custom_input = input(f"{Colors.BOLD}Enter ports separated by commas (e.g. 80,443,8080): {Colors.ENDC}").strip()
    if not custom_input:
        print(f"{Colors.FAIL}[!] No ports provided. Returning to menu.{Colors.ENDC}")
        return
    try:
        ports = [int(p.strip()) for p in custom_input.split(',')]
        print(f"\n{Colors.BLUE}[*] Running Custom Scan on {len(ports)} ports...{Colors.ENDC}")
        run_scan(target_ip, ports)
    except ValueError:
        print(f"{Colors.FAIL}[!] Invalid formatting detected. Use numeric characters and commas only.{Colors.ENDC}")

def run_scan(target_ip, ports):
    """Core scanning mechanism."""
    print(f"[*] Time started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            print(f"{Colors.GREEN}[+] Port {port} is OPEN{Colors.ENDC}")
            banner = grab_banner(target_ip, port)
            if banner:
                clean_banner = banner.replace('\r', '').replace('\n', ' | ')
                print(f"    {Colors.WARNING}└── Banner: {clean_banner}{Colors.ENDC}")
            else:
                print(f"    └── Banner: Connected, no broadcast string received.")
        s.close()

    print("-" * 60)
    print(f"{Colors.BLUE}[*] Scan cycle complete.{Colors.ENDC}\n")

def execute_operational_command():
    """Launches terminal commands directly from the script context."""
    print(f"\n{Colors.WARNING}[!] Operational Command Console Mode{Colors.ENDC}")
    print("Example raw string input: hydra -l admin -P wordlists.txt 192.168.1.1 ssh")

    cmd_string = input(f"\n{Colors.BOLD}SHARKBITE > exec: {Colors.ENDC}").strip()
    if not cmd_string:
        print(f"{Colors.FAIL}[!] Empty command string ignored.{Colors.ENDC}")
        return

    print(f"\n{Colors.BLUE}[*] Running command downstream...{Colors.ENDC}\n")
    try:
        subprocess.run(cmd_string, shell=True, check=True)
    except subprocess.CalledProcessError as err:
        print(f"\n{Colors.FAIL}[!] Process returned non-zero system return status code: {err}{Colors.ENDC}")
    except Exception as general_err:
        print(f"\n{Colors.FAIL}[!] Critical breakdown during script execution stream: {general_err}{Colors.ENDC}")

def main_menu():
    """Displays the interactive user loop selection interface."""
    while True:
        print(f"\n{Colors.BOLD}-------------------------------- SHARKBITE CONTROL INTERFACE ---------------------------------{Colors.ENDC}")
        print(" [1] Quick Recon Scan (Standard Ports)")
        print(" [2] Custom Recon Scan (Manual Entry)")
        print(" [3] Run Operational Command Natively (e.g. Hydra / System binaries)")
        print(" [4] Exit Utility")
        print("-" * 94)

        choice = input(f"{Colors.BOLD}Select an option [1-4]: {Colors.ENDC}").strip()

        if choice == '1':
            target = get_target()
            if target:
                quick_scan(target)
                input("\nPress Enter to return to the main menu...")
                os.system("clear")
        elif choice == '2':
            target = get_target()
            if target:
                custom_scan(target)
                input("\nPress Enter to return to the main menu...")
                os.system("clear")
        elif choice == '3':
            execute_operational_command()
            input("\nPress Enter to return to the main menu...")
        elif choice == '4':
            print(f"\n{Colors.WARNING}[*] Powering down SHARKBITE{Colors.ENDC}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.FAIL}[!] Invalid selection. Please pick a number from 1 to 4.{Colors.ENDC}")
            input("\nPress Enter to try again...")
            os.system("clear")

if __name__ == "__main__":
    main_menu()
