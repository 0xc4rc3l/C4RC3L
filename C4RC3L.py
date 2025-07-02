#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# C4RC3L - A simple pentesting framework console develeoped in Python by 0xc4rc3l
import cmd
import os
import random
from colorama import init, Fore, Style

init(autoreset=True)

class PentestConsole(cmd.Cmd):
    intro = Fore.CYAN + Style.BRIGHT + 'Welcome to your pentesting framework! Type help or ? to list commands.' + Style.RESET_ALL
    prompt = Fore.RED + Style.BRIGHT + 'C4RC3L > ' + Style.RESET_ALL

    global_options = {
        'target': '',
        'url': '',
        'domain': '',
    }

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
            self.global_options[opt] = val
            print(Fore.GREEN + f"[+] Set {opt} to {val} (global)" + Style.RESET_ALL)
        else:
            print(Fore.RED + 'Usage: set <option> <value> (global options: target, url, domain)' + Style.RESET_ALL)

    def complete_set(self, text, line, begidx, endidx):
        # Autocomplete for global set command
        opts = [k for k in self.global_options.keys() if k.startswith(text)]
        return opts

    def do_show(self, arg):
        'Show global options.'
        print(Fore.CYAN + 'Global options:' + Style.RESET_ALL)
        for k, v in self.global_options.items():
            print(Fore.GREEN + f'  {k:<8} = {v}' + Style.RESET_ALL)

    def do_help(self, arg):
        'List available commands in a horizontal format.'
        commands = [
            ('clear', 'Clear the terminal screen.'),
            ('exit', 'Exit the console.'),
            ('set', 'Set a global option (e.g., target, url, domain).'),
            ('show', 'Show global options.'),
            ('portscan', 'Enter the portscan module.'),
        ]
        print(Fore.CYAN + Style.BRIGHT + '\nAvailable Commands:' + Style.RESET_ALL)
        for cmd_name, desc in commands:
            print(Fore.GREEN + f'  {cmd_name:<10}' + Fore.WHITE + f' - {desc}' + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + '\nType help <command> for more info.' + Style.RESET_ALL)

    def default(self, line):
        print(Fore.RED + f'Unknown command: {line}')

    def do_portscan(self, arg):
        'Enter the portscan module.'
        from modules.portscan import run_scan
        module_prompt = Fore.RED + Style.BRIGHT + 'C4RC3L ' + Fore.BLUE + '[portscan]' + Style.RESET_ALL + ' > '
        print(Fore.YELLOW + '[*] Entered portscan module. Type help for options, exit/back to return.' + Style.RESET_ALL)
        # Default options (inherits global target)
        options = {
            'target': self.global_options['target'],
            'ports': '80,443',
            'type': 'tcp',
        }
        def portscan_complete_set(text, line, begidx, endidx):
            opts = [k for k in options.keys() if k.startswith(text)]
            return opts
        while True:
            try:
                sub_cmd = input(module_prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
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
            elif sub_cmd == 'show':
                print(Fore.CYAN + 'Current options:' + Style.RESET_ALL)
                for k, v in options.items():
                    print(Fore.GREEN + f'  {k:<8} = {v}' + Style.RESET_ALL)
            elif sub_cmd == 'scan':
                if not options['target']:
                    print(Fore.RED + 'Set a target first: set target <ip/host>' + Style.RESET_ALL)
                    continue
                try:
                    ports = [int(p) for p in options['ports'].split(',')]
                except Exception:
                    print(Fore.RED + 'Invalid ports format. Use comma-separated numbers.' + Style.RESET_ALL)
                    continue
                run_scan(options['target'], ports, options['type'])
            else:
                print(Fore.RED + f'Unknown portscan command: {sub_cmd}' + Style.RESET_ALL)

    def help_portscan_module(self):
        print(Fore.CYAN + Style.BRIGHT + '\nPortscan Module Options:' + Style.RESET_ALL)
        print(Fore.GREEN + '  scan            - Run a port scan with current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  set <opt> <val> - Set an option (target, ports, type)' + Style.RESET_ALL)
        print(Fore.GREEN + '  show            - Show current options' + Style.RESET_ALL)
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

def print_banner():
    print(random.choice(ascii_banners))

if __name__ == '__main__':
    #os.system('clear')  # Clear the terminal on Linux/macOS
    print_banner()
    PentestConsole().cmdloop()
