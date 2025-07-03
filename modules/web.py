import os
import requests
from colorama import Fore, Style
import readline

class WebModule:
    def __init__(self, global_options):
        self.options = {
            'url': global_options.get('url', ''),
            'domain': global_options.get('domain', ''),
        }
        self.global_options = global_options
        self._last_dir = os.getcwd()

    def run(self):
        import shlex
        module_prompt = Fore.RED + Style.BRIGHT + 'C4RC3L ' + Fore.BLUE + '[web]' + Style.RESET_ALL + ' > '
        print(Fore.YELLOW + '[*] Entered web module. Type help for options, exit/back to return.' + Style.RESET_ALL)
        # Save previous completer and set web module completer
        prev_completer = None
        try:
            prev_completer = readline.get_completer()
            readline.set_completer_delims(' \t\n')
            readline.parse_and_bind('tab: complete')
            readline.set_completer(self._tab_complete)
        except Exception:
            pass  # readline may not be available on all platforms
        try:
            while True:
                try:
                    sub_cmd = input(module_prompt).strip()
                except EOFError:
                    print()
                    break
                except KeyboardInterrupt:
                    print()
                    continue
                if sub_cmd in ('exit', 'back', 'quit'):
                    print(Fore.YELLOW + '[*] Exiting web module...' + Style.RESET_ALL)
                    break
                elif sub_cmd in ('help', '?', ''):
                    self.help()
                elif sub_cmd == 'clear':
                    os.system('clear')
                elif sub_cmd.startswith('set '):
                    parts = sub_cmd.split(maxsplit=2)
                    if len(parts) == 2 and parts[1] == '':
                        print('Options:', ', '.join(self.options.keys()))
                        continue
                    if len(parts) == 3 and parts[1] in self.options:
                        self.options[parts[1]] = parts[2]
                        if parts[1] in self.global_options:
                            self.global_options[parts[1]] = parts[2]
                        print(Fore.GREEN + f"[+] Set {parts[1]} to {parts[2]}" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + 'Usage: set <option> <value>' + Style.RESET_ALL)
                elif sub_cmd in ('options',):
                    print(Fore.CYAN + 'Current options:' + Style.RESET_ALL)
                    for k, v in self.options.items():
                        print(Fore.GREEN + f'  {k:<10}    =    {v}' + Style.RESET_ALL)
                elif sub_cmd == 'http_get':
                    url = self.options.get('url') or self.global_options.get('url')
                    if not url:
                        print(Fore.RED + '[!] Set url first: set url <url>' + Style.RESET_ALL)
                        continue
                    try:
                        resp = requests.get(url, timeout=10)
                        print(Fore.CYAN + f"[GET] {url}" + Style.RESET_ALL)
                        print(Fore.GREEN + f"Status: {resp.status_code}" + Style.RESET_ALL)
                        print(Fore.YELLOW + 'Headers:' + Style.RESET_ALL)
                        for k, v in resp.headers.items():
                            print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                        print(Fore.YELLOW + 'Body:' + Style.RESET_ALL)
                        print(Fore.WHITE + resp.text[:1000] + ("..." if len(resp.text) > 1000 else "") + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[!] HTTP GET failed: {e}" + Style.RESET_ALL)
                elif sub_cmd == 'http_post':
                    url = self.options.get('url') or self.global_options.get('url')
                    if not url:
                        print(Fore.RED + '[!] Set url first: set url <url>' + Style.RESET_ALL)
                        continue
                    try:
                        resp = requests.post(url, timeout=10)
                        print(Fore.CYAN + f"[POST] {url}" + Style.RESET_ALL)
                        print(Fore.GREEN + f"Status: {resp.status_code}" + Style.RESET_ALL)
                        print(Fore.YELLOW + 'Headers:' + Style.RESET_ALL)
                        for k, v in resp.headers.items():
                            print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                        print(Fore.YELLOW + 'Body:' + Style.RESET_ALL)
                        print(Fore.WHITE + resp.text[:1000] + ("..." if len(resp.text) > 1000 else "") + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[!] HTTP POST failed: {e}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f'Unknown web command: {sub_cmd}' + Style.RESET_ALL)
        finally:
            # Restore previous completer
            try:
                readline.set_completer(prev_completer)
            except Exception:
                pass

    def help(self):
        print(Fore.CYAN + Style.BRIGHT + '\nWeb Module Options:' + Style.RESET_ALL)
        print(Fore.GREEN + '  http_get        - HTTP GET request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  http_post       - HTTP POST request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  set <opt> <val> - Set an option (url, domain)' + Style.RESET_ALL)
        print(Fore.GREEN + '  options         - Show current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  clear           - Clear the terminal' + Style.RESET_ALL)
        print(Fore.GREEN + '  help/?          - Show this help menu' + Style.RESET_ALL)
        print(Fore.GREEN + '  exit/back       - Return to main console' + Style.RESET_ALL)

    def complete(self, text, line, begidx, endidx):
        cmds = ['http_get', 'http_post', 'set', 'options', 'clear', 'help', '?', 'exit', 'back']
        if begidx == 0:
            return [c for c in cmds if c.startswith(text)]
        if line.strip().startswith('set '):
            opts = [k for k in self.options.keys() if k.startswith(text)]
            return opts
        return []

    def _tab_complete(self, text, state):
        # Tab completion for web module shell
        buffer = readline.get_line_buffer()
        line = buffer.lstrip()
        begidx = len(buffer) - len(text)
        endidx = len(buffer)
        completions = self.complete(text, line, begidx, endidx)
        if state < len(completions):
            return completions[state]
        return None
