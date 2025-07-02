# modules/portscan.py
# Portscan module logic for C4RC3L framework

def run_scan(target, ports, scan_type='tcp'):
    import socket
    from colorama import Fore, Style
    print(Fore.CYAN + f"[+] Scanning {target} on ports: {ports} (type: {scan_type})" + Style.RESET_ALL)
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if scan_type == 'tcp' else socket.SOCK_DGRAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(Fore.GREEN + f"[+] Port {port} is open" + Style.RESET_ALL)
                open_ports.append(port)
            sock.close()
        except Exception as e:
            print(Fore.RED + f"[!] Error scanning port {port}: {e}" + Style.RESET_ALL)
    return open_ports
