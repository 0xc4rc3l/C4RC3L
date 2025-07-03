# modules/portscan.py
# Portscan module logic for C4RC3L framework

def run_scan(target, scan_type='tcp'):
    import subprocess
    from colorama import Fore, Style
    import re
    if scan_type == 'udp':
        nmap_args = ['nmap', '-sU', target]
    elif scan_type == 'all':
        # Scan all ports, no service/script scan
        nmap_args = ['nmap', '-sS', '-p-', target]
    else:
        nmap_args = ['nmap', '-sS', target]
    print(Fore.CYAN + f"[+] Running nmap scan: {' '.join(nmap_args)}" + Style.RESET_ALL)
    try:
        result = subprocess.run(nmap_args, capture_output=True, text=True, check=True)
        print(Fore.GREEN + result.stdout + Style.RESET_ALL)
        if scan_type in ('tcp', 'all'):
            # Parse open ports from nmap output
            open_ports = []
            for line in result.stdout.splitlines():
                # Typical nmap output: '22/tcp   open  ssh'
                m = re.match(r'^(\d+)/tcp\s+open', line)
                if m:
                    open_ports.append(int(m.group(1)))
            return open_ports
    except FileNotFoundError:
        print(Fore.RED + '[!] nmap is not installed or not found in PATH.' + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[!] nmap scan failed: {e.stderr}" + Style.RESET_ALL)
    return []

# Autocomplete for all portscan module commands

def portscan_complete(text, line, begidx, endidx):
    commands = ['scan', 'scan all', 'set', 'options', 'ports', 'clear', 'help', '?', 'exit', 'back', 'quit']
    args = line.strip().split()
    if not args or (len(args) == 1 and not text):
        # Suggest all commands at start
        return commands
    if args[0] == 'set':
        opts = ['target', 'type']
        if len(args) == 2:
            return [o for o in opts if o.startswith(text)]
        if len(args) >= 3 and args[1] == 'type':
            return [t for t in ['tcp', 'udp'] if t.startswith(text)]
    elif args[0] == 'scan':
        if len(args) == 1 and 'all'.startswith(text):
            return ['all']
    else:
        return [c for c in commands if c.startswith(text)]
    return []

# For backward compatibility, keep portscan_complete_set for set command

def portscan_complete_set(text, line, begidx, endidx):
    opts = ['target', 'type']
    args = line.split()
    if len(args) == 2 and args[0] == 'set':
        return [o for o in opts if o.startswith(text)]
    if len(args) >= 3 and args[1] == 'type':
        return [t for t in ['tcp', 'udp'] if t.startswith(text)]
    return []
