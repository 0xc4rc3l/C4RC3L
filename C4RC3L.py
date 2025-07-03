#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# C4RC3L - A simple pentesting framework console develeoped in Python by 0xc4rc3l
import cmd
import os
import random
import json
from colorama import init, Fore, Style
import sys

init(autoreset=True)

class PentestConsole(cmd.Cmd):
    prompt = Fore.RED + Style.BRIGHT + 'C4RC3L > ' + Style.RESET_ALL

    state_file_name = 'c4rc3l_state.json'
    global_options = {
        'target': '',
        'url': '',
        'domain': '',
        'dir_list': '',   # Wordlist for directory bruteforce
        'sub_list': '',   # Wordlist for subdomain bruteforce
        'file_list': '',  # Wordlist for file bruteforce
    }

    def __init__(self, workspace_dir=None):
        super().__init__()
        self._workflow_dirs = ['enu', 'files', 'exploits', 'loot']
        # logs/workspace for state/logs, workflow dirs in project root
        cwd = os.getcwd()
        logs_root = os.path.join(cwd, 'logs')
        ws_root = os.path.join(logs_root, 'workspace')
        self.workspace_dir = ws_root
        self.logs_dir = ws_root  # For state/logs only
        self._portscan_ports = []
        # Auto-detect workflow initialization
        all_dirs = [os.path.join(cwd, d) for d in self._workflow_dirs]
        if all(os.path.isdir(d) for d in all_dirs) and os.path.isdir(ws_root):
            self._workflow_initialized = True
            self._load_state()
        else:
            self._workflow_initialized = False

    @property
    def state_file(self):
        return os.path.join(self.logs_dir, self.state_file_name)

    def _load_state(self):
        if not self._workflow_initialized:
            return
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            if 'global_options' in state:
                self.global_options.update(state['global_options'])
            self._portscan_ports = state.get('portscan_ports', [])
        except Exception:
            self._portscan_ports = []

    def _save_state(self):
        if not self._workflow_initialized:
            return
        try:
            state = {
                'global_options': self.global_options,
                'portscan_ports': getattr(self, '_portscan_ports', []),
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(Fore.RED + f"[!] Failed to save state: {e}" + Style.RESET_ALL)

    def do_exit(self, arg):
        'Exit the console.'
        self._save_state()
        print(Fore.YELLOW + 'Exiting...')
        return True

    def do_clear(self, arg):
        'Clear the terminal screen.'
        os.system('clear')

    def do_set(self, arg):
        'Set a global option: set <option> <value>'
        if not self._workflow_initialized:
            print(Fore.RED + '[!] Run init first to initialize workflow and logging.' + Style.RESET_ALL)
            return
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
            self._save_state()
        else:
            print(Fore.RED + 'Usage: set <option> <value> (global options: target, url, domain, dir_list, sub_list, file_list)' + Style.RESET_ALL)

    def complete_set(self, text, line, begidx, endidx):
        # Autocomplete for global set command
        opts = [k for k in self.global_options.keys() if k.startswith(text)]
        return opts

    def do_show(self, arg):
        'Show global options.'
        if not self._workflow_initialized:
            print(Fore.RED + '[!] Run init first to initialize workflow and logging.' + Style.RESET_ALL)
            return
        self._load_state()  # Always show latest
        print(Fore.CYAN + 'Global options:' + Style.RESET_ALL)
        for k, v in self.global_options.items():
            print(Fore.GREEN + f'  {k:<10} = {v}' + Style.RESET_ALL)

    def do_init(self, arg):
        'Initialize pentest workflow directories: enu, files, exploits, loot in project root, logs/workspace for state.'
        cwd = os.getcwd()
        logs_root = os.path.join(cwd, 'logs')
        ws_root = os.path.join(logs_root, 'workspace')
        # Remove workflow dirs from logs/workspace if they exist
        for d in self._workflow_dirs:
            ws_dir = os.path.join(ws_root, d)
            if os.path.isdir(ws_dir):
                import shutil
                try:
                    shutil.rmtree(ws_dir)
                    print(Fore.YELLOW + f"[*] Removed stray workflow directory from workspace: {ws_dir}" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"[!] Failed to remove {ws_dir}: {e}" + Style.RESET_ALL)
        if not os.path.isdir(ws_root):
            os.makedirs(ws_root, exist_ok=True)
            print(Fore.GREEN + f"[+] Created workspace directory: {ws_root}" + Style.RESET_ALL)
        self.workspace_dir = ws_root
        self.logs_dir = ws_root
        dirs = [os.path.join(cwd, d) for d in self._workflow_dirs]
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
            self._load_state()  # Now load state
            self._save_state()  # Save initial state if not present
        else:
            print(Fore.YELLOW + '[*] No directories created.' + Style.RESET_ALL)
            self._workflow_initialized = all(os.path.isdir(d) for d in dirs) and os.path.isdir(ws_root)
            if self._workflow_initialized:
                self._load_state()

    def do_workspace(self, arg):
        'Show current workspace status and path.'
        cwd = os.getcwd()
        logs_root = os.path.join(cwd, 'logs')
        ws_root = os.path.join(logs_root, 'workspace')
        if os.path.isdir(ws_root):
            print(Fore.GREEN + f"[+] Workspace for logs/state: {ws_root}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"[*] No workspace found. Run 'init' to create logs/workspace for state/logs." + Style.RESET_ALL)

    def do_help(self, arg):
        'List available commands in a horizontal format.'
        commands = [
            ('clear', 'Clear the terminal screen.'),
            ('exit', 'Exit the console.'),
            ('set', 'Set a global option (e.g., target, url, domain).'),
            ('show', 'Show global options.'),
            ('init', 'Initialize workflow directories in project root and logs/workspace for state.'),
            ('workspace', 'Show workspace (logs/state) status and path.'),
            ('portscan', 'Enter the portscan module.'),
            ('web', 'Enter the web module.'),
        ]
        print(Fore.CYAN + Style.BRIGHT + '\nAvailable Commands:' + Style.RESET_ALL)
        for cmd_name, desc in commands:
            print(Fore.GREEN + f'  {cmd_name:<10}' + Fore.WHITE + f' - {desc}' + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + '\nWorkspace Usage:' + Style.RESET_ALL)
        print(Fore.WHITE + '  Workflow directories (enu, files, exploits, loot) are in the project root.' + Style.RESET_ALL)
        print(Fore.WHITE + '  All logs and state are stored in logs/workspace.' + Style.RESET_ALL)
        print(Fore.WHITE + '  To create or reset the workspace, run: init' + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + '\nType help <command> for more info.' + Style.RESET_ALL)

    def complete_cd(self, text, line, begidx, endidx):
        # Autocomplete for cd command: directories only
        import glob
        if not text:
            text = '.'
        return [d + '/' for d in glob.glob(text + '*') if os.path.isdir(d)]

    def complete_ls(self, text, line, begidx, endidx):
        # Autocomplete for ls command: files and directories
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_cat(self, text, line, begidx, endidx):
        # Autocomplete for cat command: files only
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*') if os.path.isfile(f)]

    def complete_rm(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_mv(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_cp(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_mkdir(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [d for d in glob.glob(text + '*') if os.path.isdir(d)]

    def complete_rmdir(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [d for d in glob.glob(text + '*') if os.path.isdir(d)]

    def complete_touch(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_head(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*') if os.path.isfile(f)]

    def complete_tail(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*') if os.path.isfile(f)]

    def complete_find(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_grep(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_chmod(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def complete_chown(self, text, line, begidx, endidx):
        import glob
        if not text:
            text = '.'
        return [f for f in glob.glob(text + '*')]

    def default(self, line):
        # Allow running system commands: pwd, cd, cd -, ls, cat, head, tail, cp, mv, rm, mkdir, rmdir, touch, history, whoami, ifconfig, ip, ps, kill, find, grep, chmod, chown, git, searchsploit
        import shlex
        import subprocess
        allowed = [
            'pwd', 'ls', 'cd', 'cat', 'head', 'tail', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'touch',
            'history', 'whoami', 'ifconfig', 'ip', 'ps', 'kill', 'find', 'grep', 'chmod', 'chown',
            'git', 'searchsploit'
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
                    result = subprocess.run(parts, capture_output=True, text=True)
                    if result.stdout:
                        print(result.stdout, end='')
                    if result.stderr:
                        print(Fore.YELLOW + result.stderr + Style.RESET_ALL, end='')
                    # Do not print any extra error message for nonzero exit code
            except FileNotFoundError:
                print(Fore.RED + f"[!] Command not found: {line}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f'Unknown command: {line}')

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
        options = {
            'target': self.global_options['target'],
            'type': 'tcp',
        }
        self._load_state()
        ports = list(getattr(self, '_portscan_ports', []))
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
                'history', 'whoami', 'ifconfig', 'ip', 'ps', 'kill', 'find', 'grep', 'chmod', 'chown',
                'git', 'searchsploit'
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
                    self._portscan_ports = ports
                    self._save_state()
                    if ports:
                        print(Fore.GREEN + f"[+] Open ports found: {', '.join(str(p) for p in ports)}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No open ports found.' + Style.RESET_ALL)
            elif sub_cmd == 'scan all':
                if not options['target']:
                    print(Fore.RED + 'Set a target first: set target <ip/host>' + Style.RESET_ALL)
                    continue
                result = run_scan(options['target'], 'all')
                if isinstance(result, list):
                    ports.clear()
                    ports.extend(result)
                    self._portscan_ports = ports
                    self._save_state()
                    if ports:
                        print(Fore.GREEN + f"[+] Open ports found: {', '.join(str(p) for p in ports)}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No open ports found.' + Style.RESET_ALL)
            elif sub_cmd == 'ports':
                self._load_state()
                ports = list(getattr(self, '_portscan_ports', []))
                if ports:
                    print(Fore.CYAN + '[*] Open ports from last scan:' + Style.RESET_ALL)
                    print(Fore.GREEN + ', '.join(str(p) for p in ports) + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + '[*] No open ports saved. Run scan first.' + Style.RESET_ALL)
            elif sub_cmd.startswith('service'):
                # service [name_to_save_as]
                parts = sub_cmd.split(maxsplit=1)
                if not ports:
                    print(Fore.RED + '[!] No open ports found. Run scan or scan all first.' + Style.RESET_ALL)
                    continue
                port_str = ','.join(str(p) for p in ports)
                nmap_args = ['nmap', '-sV', '-sC', '-p', port_str, options['target']]
                if len(parts) == 2 and parts[1]:
                    # Save results to enu/{name}
                    name = parts[1]
                    enu_dir = os.path.join(os.getcwd(), 'enu')
                    if not os.path.isdir(enu_dir):
                        try:
                            os.makedirs(enu_dir, exist_ok=True)
                        except Exception as e:
                            print(Fore.RED + f"[!] Failed to create enu directory: {e}" + Style.RESET_ALL)
                            continue
                    out_path = os.path.join(enu_dir, name)
                    nmap_args += ['-oA', out_path]
                    print(Fore.CYAN + f"[+] Running nmap service/script scan and saving as {out_path}.nmap/.xml/.gnmap" + Style.RESET_ALL)
                else:
                    print(Fore.CYAN + f"[+] Running nmap service/script scan: {' '.join(nmap_args)}" + Style.RESET_ALL)
                try:
                    result = subprocess.run(nmap_args, capture_output=True, text=True, check=True)
                    print(Fore.GREEN + result.stdout + Style.RESET_ALL)
                    if len(parts) == 2 and parts[1]:
                        print(Fore.GREEN + f"[+] Results saved as {out_path}.nmap/.xml/.gnmap" + Style.RESET_ALL)
                except FileNotFoundError:
                    print(Fore.RED + '[!] nmap is not installed or not found in PATH.' + Style.RESET_ALL)
                except subprocess.CalledProcessError as e:
                    print(Fore.RED + f"[!] nmap scan failed: {e.stderr}" + Style.RESET_ALL)
                continue
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
                'history', 'whoami', 'ifconfig', 'ip', 'ps', 'kill', 'find', 'grep', 'chmod', 'chown',
                'git', 'searchsploit'
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
     )\___  ((_)\u005c (_))  )\___  ((_)c (_))   
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
    # Workspace support: allow CLI arg or env var
    workspace_dir = sys.argv[1] if len(sys.argv) > 1 else None
    console = PentestConsole(workspace_dir=workspace_dir)
    while True:
        try:
            console.cmdloop(intro=None)
            break  # Exit only if do_exit returns True
        except KeyboardInterrupt:
            # Print a newline to avoid stacking prompts
            print()
            continue
