import subprocess
import sys

# ANSI color codes (no external libraries)
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

scan_logs = []

important_ports = {"80", "443", "3389"}
suspicious_ports = {"22", "23" "53", "21", "137", "139", "445", "3306", "1433"}
dangerous_ports = {"4444", "6667", "10000" "31337"}

while True:
    print("[1] Scan")
    print("[2] Display Scan Output")
    print("[7] Exit")
    usrInput = input("Choose: ")

    match usrInput:
        case "1":
            scan = ["ipconfig", "ping 8.8.8.8", "netstat -an"]
            scan_logs.clear()

            print(f"\n{CYAN}[🔍] Starting scan...{RESET}\n")

            for cmd in scan:
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout
                scan_logs.append(f"\n===== {cmd} Output =====\n{output}")

                for line in output.splitlines():
                    parts = line.split()

                    if "IPv4 Address" in line:
                        print("[IP] ", line.strip())
                    elif "Reply from" in line:
                        print("[PING] ", line.strip())
                    elif "Request timed out" in line:
                        print("[PING] ", line.strip())
                    elif cmd == "netstat -an" and len(parts) >= 4 and parts[0] in ["TCP", "UDP"]:
                        protocol = parts[0]
                        local = parts[1]
                        remote = parts[2]
                        state = parts[3] if protocol == "TCP" else "N/A"

                        if ':' in remote:
                            port = remote.rsplit(":", 1)[-1]
                        else:
                            port = ""

                        # Apply color and tag based on port type
                        if port in dangerous_ports:
                            tag = f"{RED}[🚨 suspicious]{RESET}"
                        elif port in suspicious_ports:
                            tag = f"{YELLOW}[⚠ maybe risky]{RESET}"
                        elif port in important_ports:
                            tag = f"{GREEN}[✔ important]{RESET}"
                        else:
                            continue  # Skip others

                        print(f"{CYAN}[NETSTAT]{RESET} {protocol:<5} {local:<21} -> {remote:<21} {state:<12} {tag}")

            with open("scanOutput.txt", "w") as f:
                f.write("\n".join(scan_logs))

            print(f"\n{CYAN}[✔] Scan complete. For full details, select [2] Display Scan Output.{RESET}\n")

        case "2":
            try:
                with open("scanOutput.txt", "r") as f:
                    print(f"\n{CYAN}========== Full Scan Output =========={RESET}\n")
                    print(f.read())
            except FileNotFoundError:
                print("[!] No scan data found. Please run a scan first.")

        case "7":
            sys.exit(0)

        case _:
            print("Invalid choice. Please select 1, 2, or 7.")
