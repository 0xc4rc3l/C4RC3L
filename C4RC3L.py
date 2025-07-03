#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# C4RC3L - A simple pentesting framework console develeoped in Python by 0xc4rc3l
import cmd
import os
import random
from colorama import init, Fore, Style

init(autoreset=True)

class PentestConsole(cmd.Cmd):
    prompt = Fore.RED + Style.BRIGHT + 'C4RC3L > ' + Style.RESET_ALL

    global_options = {
        'target': '',
        'url': '',
        'domain': '',
        'dir_list': '',   # Wordlist for directory bruteforce
        'sub_list': '',   # Wordlist for subdomain bruteforce
        'file_list': '',  # Wordlist for file bruteforce
    }

    def __init__(self):
        super().__init__()
        self._workflow_initialized = False
        self._workflow_dirs = ['enu', 'files', 'exploits', 'loot']

    def do_exit(self, arg):
        'Exit the console.'
        print(Fore.YELLOW + 'Exiting...')
        return True

    def do_clear(self, arg):
        'Clear the terminal screen.'
        os.system('clear')

    def do_set(self, arg):
        'Set a global option: set <option> <value>'
        parts = arg.split(maxsplit=1)
        if len(parts) == 2 and parts[0] in self.global_options:
            opt, val = parts[0], parts[1]
            if opt == 'target':
                # Validate IP address (basic check)
                import re
                ip_regex = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
                if not re.match(ip_regex, val):
                    print(Fore.RED + '[!] Invalid IP address format.' + Style.RESET_ALL)
                    return
            elif opt == 'url':
                if not (val.startswith('http://') or val.startswith('https://')):
                    val = 'http://' + val
                # Basic URL validation
                import re
                url_regex = r'^(http://|https://)[\w.-]+(?:\.[\w\.-]+)+.*$'
                if not re.match(url_regex, val):
                    print(Fore.RED + '[!] Invalid URL format.' + Style.RESET_ALL)
                    return
            elif opt == 'domain':
                # Basic domain validation
                import re
                domain_regex = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,}$'
                if not re.search(r'\.', val) or not re.match(domain_regex, val.split('.', 1)[-1]):
                    print(Fore.RED + '[!] Invalid domain format.' + Style.RESET_ALL)
                    return
            # For dir_list, sub_list, file_list: just set, no validation for now
            self.global_options[opt] = val
            print(Fore.GREEN + f"[+] Set {opt} to {val} (global)" + Style.RESET_ALL)
        else:
            print(Fore.RED + 'Usage: set <option> <value> (global options: target, url, domain, dir_list, sub_list, file_list)' + Style.RESET_ALL)

    def complete_set(self, text, line, begidx, endidx):
        # Autocomplete for global set command
        opts = [k for k in self.global_options.keys() if k.startswith(text)]
        return opts

    def do_show(self, arg):
        'Show global options.'
        print(Fore.CYAN + 'Global options:' + Style.RESET_ALL)
        for k, v in self.global_options.items():
            print(Fore.GREEN + f'  {k:<10} = {v}' + Style.RESET_ALL)

    def do_help(self, arg):
        'List available commands in a horizontal format.'
        commands = [
            ('clear', 'Clear the terminal screen.'),
            ('exit', 'Exit the console.'),
            ('set', 'Set a global option (e.g., target, url, domain).'),
            ('show', 'Show global options.'),
            ('init', 'Initialize workflow directories (enu, files, exploits, loot).'),
            ('portscan', 'Enter the portscan module.'),
            ('web', 'Enter the web module.'),
        ]
        print(Fore.CYAN + Style.BRIGHT + '\nAvailable Commands:' + Style.RESET_ALL)
        for cmd_name, desc in commands:
            print(Fore.GREEN + f'  {cmd_name:<10}' + Fore.WHITE + f' - {desc}' + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + '\nType help <command> for more info.' + Style.RESET_ALL)

    def default(self, line):
        # Allow running system commands: pwd, cd, cd -, ls, cat, head, tail, cp, mv, rm, mkdir, rmdir, touch, history, whoami, ifconfig, ip, ps, kill, find, grep, chmod, chown
        import shlex
        from subprocess import run, CalledProcessError
        allowed = [
            'pwd', 'ls', 'cd', 'cat', 'head', 'tail', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'touch',
            'history', 'whoami', 'ifconfig', 'ip', 'ps', 'kill', 'find', 'grep', 'chmod', 'chown'
        ]
        if not hasattr(self, '_last_dir'):
            self._last_dir = os.getcwd()
        parts = shlex.split(line)
        if parts and (parts[0] in allowed or (parts[0] == 'ip' and len(parts) > 1 and parts[1] == 'a')):
            try:
                if parts[0] == 'cd':
                    if len(parts) > 1:
                        if parts[1] == '-':
                            current = os.getcwd()
                            os.chdir(self._last_dir)
                            print(f"Changed directory to {os.getcwd()}")
                            self._last_dir = current
                        else:
                            current = os.getcwd()
                            os.chdir(parts[1])
                            print(f"Changed directory to {os.getcwd()}")
                            self._last_dir = current
                    else:
                        print(os.getcwd())
                else:
                    result = run(parts, check=True)
            except FileNotFoundError:
                print(Fore.RED + f"[!] Command not found: {line}" + Style.RESET_ALL)
            except CalledProcessError as e:
                print(Fore.RED + f"[!] Command failed: {e}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f'Unknown command: {line}')

    def do_init(self, arg):
        'Initialize pentest workflow directories: enu, files, exploits, loot.'
        dirs = self._workflow_dirs
        created = []
        for d in dirs:
            try:
                os.makedirs(d, exist_ok=True)
                created.append(d)
            except Exception as e:
                print(Fore.RED + f"[!] Failed to create {d}: {e}" + Style.RESET_ALL)
        if created:
            print(Fore.GREEN + f"[+] Initialized directories: {', '.join(created)}" + Style.RESET_ALL)
            self._workflow_initialized = True
        else:
            print(Fore.YELLOW + '[*] No directories created.' + Style.RESET_ALL)
            self._workflow_initialized = all(os.path.isdir(d) for d in dirs)

    def do_portscan(self, arg):
        'Enter the portscan module.'
        if not getattr(self, '_workflow_initialized', False):
            print(Fore.RED + '[!] Run init first to initialize workflow directories.' + Style.RESET_ALL)
            return
        from modules.portscan import run_scan
        import subprocess
        import shlex
        module_prompt = Fore.RED + Style.BRIGHT + 'C4RC3L ' + Fore.BLUE + '[portscan]' + Style.RESET_ALL + ' > '
        print(Fore.YELLOW + '[*] Entered portscan module. Type help for options, exit/back to return.' + Style.RESET_ALL)
        # Default options (inherits global target)
        options = {
            'target': self.global_options['target'],
            'type': 'tcp',
        }
        ports = []  # Store open ports found in this session
        if not hasattr(self, '_last_dir'):
            self._last_dir = os.getcwd()
        def portscan_complete_set(text, line, begidx, endidx):
            opts = [k for k in options.keys() if k.startswith(text)]
            # Autocomplete for scan type
            args = line.split()
            if len(args) >= 3 and args[1] == 'type':
                return [t for t in ['tcp', 'udp'] if t.startswith(text)]
            return opts
        while True:
            try:
                sub_cmd = input(module_prompt).strip()
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()  # Print newline, stay in module
                continue
            # System commands in module
            allowed = [
                'pwd', 'ls', 'cd', 'cat', 'head', 'tail', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'touch',
                'history', 'whoami', 'ifconfig', 'ip', 'ps', 'kill', 'find', 'grep', 'chmod', 'chown'
            ]
            sys_parts = shlex.split(sub_cmd)
            if sys_parts and (sys_parts[0] in allowed or (sys_parts[0] == 'ip' and len(sys_parts) > 1 and sys_parts[1] == 'a')):
                try:
                    if sys_parts[0] == 'cd':
                        if len(sys_parts) > 1:
                            if sys_parts[1] == '-':
                                current = os.getcwd()
                                os.chdir(self._last_dir)
                                print(f"Changed directory to {os.getcwd()}")
                                self._last_dir = current
                            else:
                                current = os.getcwd()
                                os.chdir(sys_parts[1])
                                print(f"Changed directory to {os.getcwd()}")
                                self._last_dir = current
                        else:
                            print(os.getcwd())
                    else:
                        result = subprocess.run(sys_parts, check=True)
                except FileNotFoundError:
                    print(Fore.RED + f"[!] Command not found: {sub_cmd}" + Style.RESET_ALL)
                except subprocess.CalledProcessError as e:
                    print(Fore.RED + f"[!] Command failed: {e}" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
                continue
            if sub_cmd in ('exit', 'back', 'quit'):
                print(Fore.YELLOW + '[*] Exiting portscan module...' + Style.RESET_ALL)
                break
            elif sub_cmd in ('help', '?', ''):
                self.help_portscan_module()
            elif sub_cmd == 'clear':
                os.system('clear')
            elif sub_cmd.startswith('set '):
                # set <option> <value>
                parts = sub_cmd.split(maxsplit=2)
                if len(parts) == 2 and parts[1] == '':
                    # Autocomplete options for set
                    print('Options:', ', '.join(portscan_complete_set('', '', 0, 0)))
                    continue
                if len(parts) == 3 and parts[1] in options:
                    options[parts[1]] = parts[2]
                    if parts[1] == 'target':
                        self.global_options['target'] = parts[2]
                    print(Fore.GREEN + f"[+] Set {parts[1]} to {parts[2]}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + 'Usage: set <option> <value>' + Style.RESET_ALL)
            elif sub_cmd in ('options',):
                print(Fore.CYAN + 'Current options:' + Style.RESET_ALL)
                for k, v in options.items():
                    print(Fore.GREEN + f'  {k:<10}    =    {v}' + Style.RESET_ALL)
            elif sub_cmd == 'scan':
                if not options['target']:
                    print(Fore.RED + 'Set a target first: set target <ip/host>' + Style.RESET_ALL)
                    continue
                result = run_scan(options['target'], options['type'])
                if options['type'] == 'tcp' and isinstance(result, list):
                    ports.clear()
                    ports.extend(result)
                    if ports:
                        print(Fore.GREEN + f"[+] Open ports found: {', '.join(str(p) for p in ports)}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No open ports found.' + Style.RESET_ALL)
            elif sub_cmd == 'scan all':
                if not options['target']:
                    print(Fore.RED + 'Set a target first: set target <ip/host>' + Style.RESET_ALL)
                    continue
                # Scan all ports (1-65535), no service/script scan
                result = run_scan(options['target'], 'all')
                if isinstance(result, list):
                    ports.clear()
                    ports.extend(result)
                    if ports:
                        print(Fore.GREEN + f"[+] Open ports found: {', '.join(str(p) for p in ports)}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No open ports found.' + Style.RESET_ALL)
            elif sub_cmd == 'service':
                if not ports:
                    print(Fore.RED + '[!] No open ports found. Run scan or scan all first.' + Style.RESET_ALL)
                    continue
                # Run nmap service and script scan on found ports
                port_str = ','.join(str(p) for p in ports)
                nmap_args = ['nmap', '-sV', '-sC', '-p', port_str, options['target']]
                print(Fore.CYAN + f"[+] Running nmap service/script scan: {' '.join(nmap_args)}" + Style.RESET_ALL)
                try:
                    result = subprocess.run(nmap_args, capture_output=True, text=True, check=True)
                    print(Fore.GREEN + result.stdout + Style.RESET_ALL)
                except FileNotFoundError:
                    print(Fore.RED + '[!] nmap is not installed or not found in PATH.' + Style.RESET_ALL)
                except subprocess.CalledProcessError as e:
                    print(Fore.RED + f"[!] nmap scan failed: {e.stderr}" + Style.RESET_ALL)
            elif sub_cmd == 'ports':
                if ports:
                    print(Fore.CYAN + '[*] Open ports from last scan:' + Style.RESET_ALL)
                    print(Fore.GREEN + ', '.join(str(p) for p in ports) + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + '[*] No open ports saved. Run scan first.' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Unknown portscan command: {sub_cmd}' + Style.RESET_ALL)

    def help_portscan_module(self):
        print(Fore.CYAN + Style.BRIGHT + '\nPortscan Module Options:' + Style.RESET_ALL)
        print(Fore.GREEN + '  scan            - Run a port scan with current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  scan all        - Scan all ports (no service/script scan)' + Style.RESET_ALL)
        print(Fore.GREEN + '  service         - Service and script scan on open ports' + Style.RESET_ALL)
        print(Fore.GREEN + '  set <opt> <val> - Set an option (target, type)' + Style.RESET_ALL)
        print(Fore.GREEN + '  options         - Show current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  clear           - Clear the terminal' + Style.RESET_ALL)
        print(Fore.GREEN + '  help/?          - Show this help menu' + Style.RESET_ALL)
        print(Fore.GREEN + '  exit/back       - Return to main console' + Style.RESET_ALL)

    def do_web(self, arg):
        'Enter the web module.'
        if not getattr(self, '_workflow_initialized', False):
            print(Fore.RED + '[!] Run init first to initialize workflow directories.' + Style.RESET_ALL)
            return
        # Placeholder for future web module import and logic
        import shlex
        import subprocess
        module_prompt = Fore.RED + Style.BRIGHT + 'C4RC3L ' + Fore.BLUE + '[web]' + Style.RESET_ALL + ' > '
        print(Fore.YELLOW + '[*] Entered web module. Type help for options, exit/back to return.' + Style.RESET_ALL)
        # Default options (inherits global url and domain)
        options = {
            'url': self.global_options['url'],
            'domain': self.global_options['domain'],
        }
        if not hasattr(self, '_last_dir'):
            self._last_dir = os.getcwd()
        def web_complete_set(text, line, begidx, endidx):
            opts = [k for k in options.keys() if k.startswith(text)]
            return opts
        while True:
            try:
                sub_cmd = input(module_prompt).strip()
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()  # Print newline, stay in module
                continue
            # System commands in module
            allowed = [
                'pwd', 'ls', 'cd', 'cat', 'head', 'tail', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'touch',
                'history', 'whoami', 'ifconfig', 'ip', 'ps', 'kill', 'find', 'grep', 'chmod', 'chown'
            ]
            sys_parts = shlex.split(sub_cmd)
            if sys_parts and (sys_parts[0] in allowed or (sys_parts[0] == 'ip' and len(sys_parts) > 1 and sys_parts[1] == 'a')):
                try:
                    if sys_parts[0] == 'cd':
                        if len(sys_parts) > 1:
                            if sys_parts[1] == '-':
                                current = os.getcwd()
                                os.chdir(self._last_dir)
                                print(f"Changed directory to {os.getcwd()}")
                                self._last_dir = current
                            else:
                                current = os.getcwd()
                                os.chdir(sys_parts[1])
                                print(f"Changed directory to {os.getcwd()}")
                                self._last_dir = current
                        else:
                            print(os.getcwd())
                    else:
                        result = subprocess.run(sys_parts, check=True)
                except FileNotFoundError:
                    print(Fore.RED + f"[!] Command not found: {sub_cmd}" + Style.RESET_ALL)
                except subprocess.CalledProcessError as e:
                    print(Fore.RED + f"[!] Command failed: {e}" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
                continue
            if sub_cmd in ('exit', 'back', 'quit'):
                print(Fore.YELLOW + '[*] Exiting web module...' + Style.RESET_ALL)
                break
            elif sub_cmd in ('help', '?', ''):
                self.help_web_module()
            elif sub_cmd == 'clear':
                os.system('clear')
            elif sub_cmd.startswith('set '):
                # set <option> <value>
                parts = sub_cmd.split(maxsplit=2)
                if len(parts) == 2 and parts[1] == '':
                    print('Options:', ', '.join(web_complete_set('', '', 0, 0)))
                    continue
                if len(parts) == 3 and parts[1] in options:
                    options[parts[1]] = parts[2]
                    if parts[1] in self.global_options:
                        self.global_options[parts[1]] = parts[2]
                    print(Fore.GREEN + f"[+] Set {parts[1]} to {parts[2]}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + 'Usage: set <option> <value>' + Style.RESET_ALL)
            elif sub_cmd in ('options',):
                print(Fore.CYAN + 'Current options:' + Style.RESET_ALL)
                for k, v in options.items():
                    print(Fore.GREEN + f'  {k:<10}    =    {v}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Unknown web command: {sub_cmd}' + Style.RESET_ALL)

    def help_web_module(self):
        print(Fore.CYAN + Style.BRIGHT + '\nWeb Module Options:' + Style.RESET_ALL)
        print(Fore.GREEN + '  set <opt> <val> - Set an option (url, domain)' + Style.RESET_ALL)
        print(Fore.GREEN + '  options         - Show current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  clear           - Clear the terminal' + Style.RESET_ALL)
        print(Fore.GREEN + '  help/?          - Show this help menu' + Style.RESET_ALL)
        print(Fore.GREEN + '  exit/back       - Return to main console' + Style.RESET_ALL)

# === ASCII ART BANNERS SECTION ===
# Add your ASCII art banners as strings in this list, using colorama for color if desired.
ascii_banners = [
    Fore.RED + Style.BRIGHT + r"""
      /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$   /$$$$$$  /$$      
     /$$__  $$| $$  | $$| $$__  $$ /$$__  $$ /$$__  $$| $$      
    | $$  \__/| $$  | $$| $$  \ $$| $$  \__/|__/  \ $$| $$      
    | $$      | $$$$$$$$| $$$$$$$/| $$         /$$$$$/| $$      
    | $$      |_____  $$| $$__  $$| $$        |___  $$| $$      
    | $$    $$      | $$| $$  \ $$| $$    $$ /$$  \ $$| $$      
    |  $$$$$$/      | $$| $$  | $$|  $$$$$$/|  $$$$$$/| $$$$$$$$
     \______/       |__/|__/  |__/ \______/  \______/ |________/                                                            
""" + Style.RESET_ALL,
    Fore.GREEN + Style.BRIGHT + r"""
    .------..------..------..------..------..------.
    |C.--. ||4.--. ||R.--. ||C.--. ||3.--. ||L.--. |
    | :/\: || :/\: || :(): || :/\: || :(): || :/\: |
    | :\/: || :\/: || ()() || :\/: || ()() || (__) |
    | '--'C|| '--'4|| '--'R|| '--'C|| '--'3|| '--'L|
    `------'`------'`------'`------'`------'`------'
""" + Style.RESET_ALL,
    Fore.CYAN + Style.BRIGHT + r"""
                   (                  (     
       (        )  )\ )   (        )  )\ )  
       )\    ( /( (()/(   )\    ( /( (()/(  
     (((_)   )\()) /(_))(((_)   )\()) /(_)) 
     )\___  ((_)\ (_))  )\___  ((_)\ (_))   
    ((/ __|| | (_)| _ \((/ __||__ (_)| |    
     | (__ |_  _| |   / | (__  |_ \  | |__  
      \___|  |_|  |_|_\  \___||___/  |____|
""" + Style.RESET_ALL,
    Fore.RED + Style.BRIGHT + r"""
     ▄████▄   ▄▄▄       ██▀███   ▄████▄  ▓█████  ██▓    
    ▒██▀ ▀█  ▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ ▓██▒    
    ▒▓█    ▄ ▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒███   ▒██░    
    ▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ ▒██░    
    ▒ ▓███▀ ░ ▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░░▒████▒░██████▒
    ░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░░ ▒░▓  ░
      ░  ▒     ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒    ░ ░  ░░ ░ ▒  ░
    ░          ░   ▒     ░░   ░ ░           ░     ░ ░   
    ░ ░            ░  ░   ░     ░ ░         ░  ░    ░  ░
    ░                           ░                       
""" + Style.RESET_ALL,
    Fore.BLUE + Style.BRIGHT + r"""
     ██████╗██╗  ██╗██████╗  ██████╗██████╗ ██╗     
    ██╔════╝██║  ██║██╔══██╗██╔════╝╚════██╗██║     
    ██║     ███████║██████╔╝██║      █████╔╝██║     
    ██║     ╚════██║██╔══██╗██║      ╚═══██╗██║     
    ╚██████╗     ██║██║  ██║╚██████╗██████╔╝███████╗
     ╚═════╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═════╝ ╚══════╝
""" + Style.RESET_ALL,
]
# === END OF ASCII ART BANNERS SECTION ===

def print_banner_and_intro():
    print(random.choice(ascii_banners))
    print(Fore.CYAN + Style.BRIGHT + 'Welcome to your pentesting framework! Type help or ? to list commands.' + Style.RESET_ALL)

if __name__ == '__main__':
    print_banner_and_intro()
    console = PentestConsole()
    while True:
        try:
            console.cmdloop(intro=None)
            break  # Exit only if do_exit returns True
        except KeyboardInterrupt:
            # Print a newline to avoid stacking prompts
            print()
            continue
