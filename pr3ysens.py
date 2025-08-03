import subprocess
import sys
import time
import ctypes

# Color
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

important_ports = {"80", "443", "3389"}
suspicious_ports = {"22", "23", "53", "21", "137", "139", "445", "3306", "1433"}
dangerous_ports = {"4444", "6667", "10000", "31337"}

def print_progress(current, total, task):
    percent = int((current / total) * 100)
    bar = "#" * (percent // 5) + "-" * (20 - percent // 5)
    sys.stdout.write(f"\r{CYAN}[🔄] {task:<15} [{bar}] {percent}%{RESET}")
    sys.stdout.flush()

scan_commands = [
    "ipconfig",
    "ping 8.8.8.8",
    "netstat -an",
    "systeminfo",
    "sfc /scannow",
    "dism /Online /Cleanup-Image /ScanHealth",
    "chkdsk C:"
]

def run_scan():
    if not is_admin():
        print(f"{YELLOW}[⚠] For best results, run this tool as Administrator in CMD.{RESET}")
        return

    total_cmds = len(scan_commands)
    scan_logs = []
    print(f"{CYAN}[🔍] Starting scan ...{RESET}")

    start_time = time.time()

    for i, cmd in enumerate(scan_commands, 1):
        print_progress(i - 1, total_cmds, "Scanning")
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        scan_logs.append(f"\n===== {cmd} Output =====\n{output}")

        if cmd == "netstat -an":
            detected = 0
            for line in output.splitlines():
                parts = line.split()
                if len(parts) >= 4 and parts[0] in ["TCP", "UDP"]:
                    remote = parts[2]
                    if ':' in remote:
                        port = remote.rsplit(":", 1)[-1]
                        if port in dangerous_ports:
                            print(f"{RED}[NETSTAT] Suspicious port detected: {remote}{RESET}")
                            detected += 1
                        elif port in suspicious_ports:
                            print(f"{YELLOW}[NETSTAT] Risky port detected: {remote}{RESET}")
                            detected += 1
            if detected == 0:
                print(f"{GREEN}[NETSTAT] No suspicious connections detected.{RESET}")

        elif cmd in ["systeminfo", "sfc /scannow", "dism /Online /Cleanup-Image /ScanHealth", "chkdsk C:"]:
            if "corrupt" in output.lower() or "error" in output.lower():
                print(f"{RED}[{cmd}] Issues found. Check logs for details.{RESET}")
            else:
                print(f"{GREEN}[{cmd}] No issues detected.{RESET}")

    print_progress(total_cmds, total_cmds, "Scanning")
    duration = int(time.time() - start_time)
    print(f"\n\n{CYAN}[✔] Scan complete in {duration} seconds. Use option [2] to view full logs.{RESET}")

    with open("scanOutput.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(scan_logs))

def show_menu():
    while True:
        print("\n=== pr3ysens Tool ===")
        print("[1] Full Scan")
        print("[2] Display Scan Output")
        print("[3] Exit")
        choice = input("Select an option: ")

        match choice:
            case "1":
                run_scan()
            case "2":
                try:
                    with open("scanOutput.txt", "r", encoding="utf-8") as f:
                        print(f"\n{CYAN}===== Full Scan Output ====={RESET}")
                        print(f.read())
                except FileNotFoundError:
                    print(f"{RED}[!] No scan results found. Please run a scan first.{RESET}")
            case "3":
                print("Exiting...")
                sys.exit(0)
            case _:
                print("Invalid choice. Please select 1, 2, or 3.")

# Start menu
show_menu()
