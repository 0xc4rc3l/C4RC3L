# modules/portscan.py
# Portscan module logic for C4RC3L framework

def run_scan(target, scan_type='tcp'):
    import subprocess
    from colorama import Fore, Style
    if scan_type == 'udp':
        nmap_args = ['nmap', '-sU', target]
    else:
        nmap_args = ['nmap', '-sS', target]
    print(Fore.CYAN + f"[+] Running nmap scan: {' '.join(nmap_args)}" + Style.RESET_ALL)
    try:
        result = subprocess.run(nmap_args, capture_output=True, text=True, check=True)
        print(Fore.GREEN + result.stdout + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + '[!] nmap is not installed or not found in PATH.' + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[!] nmap scan failed: {e.stderr}" + Style.RESET_ALL)

# Add autocomplete helper for portscan module

def portscan_complete_set(text, line, begidx, endidx):
    opts = ['target', 'type']
    # If completing the option name (first arg after 'set')
    args = line.split()
    if len(args) == 2 and args[0] == 'set':
        return [o for o in opts if o.startswith(text)]
    # If completing the value for 'type'
    if len(args) >= 3 and args[1] == 'type':
        return [t for t in ['tcp', 'udp'] if t.startswith(text)]
    return []
