import os
import requests
from colorama import Fore, Style
import readline
import re

def color_status(code):
    try:
        code = int(code)
    except Exception:
        return Fore.WHITE + str(code) + Style.RESET_ALL
    if 200 <= code < 300:
        return Fore.GREEN + str(code) + Style.RESET_ALL
    elif 300 <= code < 400:
        return Fore.CYAN + str(code) + Style.RESET_ALL
    elif 400 <= code < 500:
        return Fore.YELLOW + str(code) + Style.RESET_ALL
    elif 500 <= code < 600:
        return Fore.RED + str(code) + Style.RESET_ALL
    else:
        return Fore.WHITE + str(code) + Style.RESET_ALL

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
                    try:
                        os.system('clear')
                    except Exception:
                        print('\n' * 100)
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
                elif sub_cmd == 'http_head':
                    url = self.options.get('url') or self.global_options.get('url')
                    if not url:
                        print(Fore.RED + '[!] Set url first: set url <url>' + Style.RESET_ALL)
                        continue
                    try:
                        resp = requests.head(url, timeout=10)
                        print(Fore.CYAN + f"[HEAD] {url}" + Style.RESET_ALL)
                        print(Fore.GREEN + f"Status: {resp.status_code}" + Style.RESET_ALL)
                        print(Fore.YELLOW + 'Headers:' + Style.RESET_ALL)
                        for k, v in resp.headers.items():
                            print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[!] HTTP HEAD failed: {e}" + Style.RESET_ALL)
                elif sub_cmd == 'http_options':
                    url = self.options.get('url') or self.global_options.get('url')
                    if not url:
                        print(Fore.RED + '[!] Set url first: set url <url>' + Style.RESET_ALL)
                        continue
                    try:
                        resp = requests.options(url, timeout=10)
                        print(Fore.CYAN + f"[OPTIONS] {url}" + Style.RESET_ALL)
                        print(Fore.GREEN + f"Status: {resp.status_code}" + Style.RESET_ALL)
                        allow = resp.headers.get('Allow')
                        if allow:
                            print(Fore.YELLOW + 'Allowed Methods:' + Style.RESET_ALL)
                            print(Fore.WHITE + allow + Style.RESET_ALL)
                        else:
                            print(Fore.YELLOW + '[*] No Allow header found.' + Style.RESET_ALL)
                        print(Fore.YELLOW + 'Headers:' + Style.RESET_ALL)
                        for k, v in resp.headers.items():
                            print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[!] HTTP OPTIONS failed: {e}" + Style.RESET_ALL)
                elif sub_cmd == 'spider':
                    url = self.options.get('url') or self.global_options.get('url')
                    if not url:
                        print(Fore.RED + '[!] Set url first: set url <url>' + Style.RESET_ALL)
                        continue
                    from urllib.parse import urljoin, urlparse
                    from bs4 import BeautifulSoup
                    visited = set()
                    to_visit = [url]
                    found_links = []
                    enu_dir = os.path.join(os.getcwd(), 'enu')
                    web_dir = os.path.join(enu_dir, 'web')
                    html_dir = os.path.join(web_dir, 'html')
                    css_dir = os.path.join(web_dir, 'css')
                    js_dir = os.path.join(web_dir, 'js')
                    extras_dir = os.path.join(web_dir, 'extras')
                    for d in [enu_dir, web_dir, html_dir, css_dir, js_dir, extras_dir]:
                        if not os.path.isdir(d):
                            os.makedirs(d, exist_ok=True)
                    spider_out = os.path.join(enu_dir, 'spider.txt')
                    print(Fore.YELLOW + f"[*] Spidering from {url}..." + Style.RESET_ALL)
                    # Check for special files
                    special_files = ['robots.txt', 'sitemap.xml', '.DS_Store']
                    base = url.split('?', 1)[0].split('#', 1)[0]
                    if not base.endswith('/'):
                        base = base.rsplit('/', 1)[0] + '/'
                    def safe_filename(u):
                        p = urlparse(u)
                        fname = os.path.basename(p.path)
                        if not fname:
                            fname = 'index.html'
                        if '?' in fname:
                            fname = fname.split('?', 1)[0]
                        if '#' in fname:
                            fname = fname.split('#', 1)[0]
                        # Remove dangerous chars
                        fname = fname.replace('/', '_').replace('..', '_')
                        return fname
                    try:
                        with open(spider_out, 'w') as outf:
                            # Check special files
                            for fname in special_files:
                                special_url = urljoin(base, fname)
                                try:
                                    resp = requests.get(special_url, timeout=10, allow_redirects=True)
                                    code = resp.status_code
                                    if code == 200:
                                        print(f"{color_status(code)}:{special_url}")
                                        outf.write(f"{code}:{special_url}\n")
                                        found_links.append(special_url)
                                        # Save to extras
                                        outpath = os.path.join(extras_dir, fname)
                                        with open(outpath, 'wb') as f:
                                            f.write(resp.content)
                                except Exception:
                                    pass
                            # Crawl links
                            while to_visit:
                                current = to_visit.pop(0)
                                if current in visited:
                                    continue
                                visited.add(current)
                                try:
                                    resp = requests.get(current, timeout=10, allow_redirects=True)
                                    code = resp.status_code
                                except Exception as e:
                                    print(Fore.RED + f"[!] Failed to fetch {current}: {e}" + Style.RESET_ALL)
                                    continue
                                print(f"{color_status(code)}:{current}")
                                outf.write(f"{code}:{current}\n")
                                found_links.append(current)
                                ctype = resp.headers.get('Content-Type', '').split(';')[0].strip().lower()
                                # Save by type
                                fname = safe_filename(current)
                                if ctype == 'text/html' or fname.endswith('.html'):
                                    outpath = os.path.join(html_dir, fname if fname.endswith('.html') else fname + '.html')
                                    with open(outpath, 'wb') as f:
                                        f.write(resp.content)
                                elif ctype == 'text/css' or fname.endswith('.css'):
                                    outpath = os.path.join(css_dir, fname if fname.endswith('.css') else fname + '.css')
                                    with open(outpath, 'wb') as f:
                                        f.write(resp.content)
                                elif ctype in ('application/javascript', 'text/javascript') or fname.endswith('.js'):
                                    outpath = os.path.join(js_dir, fname if fname.endswith('.js') else fname + '.js')
                                    with open(outpath, 'wb') as f:
                                        f.write(resp.content)
                                # Parse HTML for more links
                                if 'text/html' in ctype:
                                    soup = BeautifulSoup(resp.text, 'html.parser')
                                    for tag in soup.find_all(['a', 'link', 'script', 'img', 'form']):
                                        href = tag.get('href') or tag.get('src') or tag.get('action')
                                        if not href:
                                            continue
                                        new_url = urljoin(current, href)
                                        # Only crawl same domain
                                        if urlparse(new_url).netloc == urlparse(url).netloc:
                                            if new_url not in visited and new_url not in to_visit:
                                                to_visit.append(new_url)
                    except Exception as e:
                        print(Fore.RED + f"[!] Spider failed: {e}" + Style.RESET_ALL)
                    print(Fore.GREEN + f"[+] Spider complete. {len(found_links)} links written to enu/spider.txt" + Style.RESET_ALL)
                elif sub_cmd.startswith('!'):
                    # Run system command
                    import subprocess
                    try:
                        result = subprocess.run(sub_cmd[1:], shell=True, capture_output=True, text=True)
                        if result.stdout:
                            print(result.stdout, end='')
                        if result.stderr:
                            print(Fore.RED + result.stderr + Style.RESET_ALL, end='')
                    except Exception as e:
                        print(Fore.RED + f"[!] System command failed: {e}" + Style.RESET_ALL)
                elif sub_cmd == 'ls' or sub_cmd == 'ls -la':
                    import subprocess
                    try:
                        result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
                        if result.stdout:
                            print(result.stdout, end='')
                        if result.stderr:
                            print(Fore.RED + result.stderr + Style.RESET_ALL, end='')
                    except Exception as e:
                        print(Fore.RED + f"[!] ls -la failed: {e}" + Style.RESET_ALL)
                elif sub_cmd.startswith('cat '):
                    import subprocess
                    try:
                        parts = sub_cmd.split(maxsplit=1)
                        if len(parts) == 2:
                            filename = parts[1]
                            result = subprocess.run(['cat', filename], capture_output=True, text=True)
                            if result.stdout:
                                print(result.stdout, end='')
                            if result.stderr:
                                print(Fore.RED + result.stderr + Style.RESET_ALL, end='')
                        else:
                            print(Fore.RED + 'Usage: cat <filename>' + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[!] cat failed: {e}" + Style.RESET_ALL)
                elif sub_cmd == 'tree':
                    import subprocess
                    try:
                        result = subprocess.run(['tree'], capture_output=True, text=True)
                        if result.stdout:
                            print(result.stdout, end='')
                        if result.stderr:
                            print(Fore.RED + result.stderr + Style.RESET_ALL, end='')
                    except Exception as e:
                        print(Fore.RED + f"[!] tree failed: {e}" + Style.RESET_ALL)
                elif sub_cmd.strip() == 'html':
                    html_dir = os.path.join(os.getcwd(), 'enu', 'web', 'html')
                    spider_txt = os.path.join(os.getcwd(), 'enu', 'spider.txt')
                    url_map = {}
                    if os.path.isfile(spider_txt):
                        with open(spider_txt, 'r') as f:
                            for line in f:
                                if ':' in line:
                                    code, url = line.strip().split(':', 1)
                                    fname = os.path.basename(url.split('?', 1)[0].split('#', 1)[0])
                                    url_map[fname] = url
                    def highlight_html_comments(text):
                        return re.sub(r'(<!--.*?-->)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, text, flags=re.DOTALL)
                    if os.path.isdir(html_dir):
                        files = sorted(os.listdir(html_dir))
                        if not files:
                            print(Fore.YELLOW + '[*] No HTML files found.' + Style.RESET_ALL)
                        for filename in files:
                            html_path = os.path.join(html_dir, filename)
                            url_found = url_map.get(filename)
                            if url_found:
                                print(Fore.CYAN + f"URL: {url_found}" + Style.RESET_ALL)
                            else:
                                print(Fore.YELLOW + f"[?] URL not found for {filename}" + Style.RESET_ALL)
                            print(Fore.GREEN + f"\n--- {filename} ---\n" + Style.RESET_ALL)
                            try:
                                with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
                                    content = f.read()
                                    print(highlight_html_comments(content))
                            except Exception as e:
                                print(Fore.RED + f"[!] Could not read {filename}: {e}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No HTML directory found.' + Style.RESET_ALL)
                elif sub_cmd.strip() == 'css':
                    css_dir = os.path.join(os.getcwd(), 'enu', 'web', 'css')
                    spider_txt = os.path.join(os.getcwd(), 'enu', 'spider.txt')
                    url_map = {}
                    if os.path.isfile(spider_txt):
                        with open(spider_txt, 'r') as f:
                            for line in f:
                                if ':' in line:
                                    code, url = line.strip().split(':', 1)
                                    fname = os.path.basename(url.split('?', 1)[0].split('#', 1)[0])
                                    url_map[fname] = url
                    def highlight_css_comments(text):
                        return re.sub(r'(/\*.*?\*/)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, text, flags=re.DOTALL)
                    if os.path.isdir(css_dir):
                        files = sorted(os.listdir(css_dir))
                        if not files:
                            print(Fore.YELLOW + '[*] No CSS files found.' + Style.RESET_ALL)
                        for filename in files:
                            css_path = os.path.join(css_dir, filename)
                            url_found = url_map.get(filename)
                            if url_found:
                                print(Fore.CYAN + f"URL: {url_found}" + Style.RESET_ALL)
                            else:
                                print(Fore.YELLOW + f"[?] URL not found for {filename}" + Style.RESET_ALL)
                            print(Fore.GREEN + f"\n--- {filename} ---\n" + Style.RESET_ALL)
                            try:
                                with open(css_path, 'r', encoding='utf-8', errors='replace') as f:
                                    content = f.read()
                                    print(highlight_css_comments(content))
                            except Exception as e:
                                print(Fore.RED + f"[!] Could not read {filename}: {e}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No CSS directory found.' + Style.RESET_ALL)
                elif sub_cmd.strip() == 'js':
                    js_dir = os.path.join(os.getcwd(), 'enu', 'web', 'js')
                    spider_txt = os.path.join(os.getcwd(), 'enu', 'spider.txt')
                    url_map = {}
                    if os.path.isfile(spider_txt):
                        with open(spider_txt, 'r') as f:
                            for line in f:
                                if ':' in line:
                                    code, url = line.strip().split(':', 1)
                                    fname = os.path.basename(url.split('?', 1)[0].split('#', 1)[0])
                                    url_map[fname] = url
                    def highlight_js_comments(text):
                        # Highlight /* ... */ and // ... comments
                        text = re.sub(r'(/\*.*?\*/)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, text, flags=re.DOTALL)
                        text = re.sub(r'(//.*?$)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, text, flags=re.MULTILINE)
                        return text
                    if os.path.isdir(js_dir):
                        files = sorted(os.listdir(js_dir))
                        if not files:
                            print(Fore.YELLOW + '[*] No JS files found.' + Style.RESET_ALL)
                        for filename in files:
                            js_path = os.path.join(js_dir, filename)
                            url_found = url_map.get(filename)
                            if url_found:
                                print(Fore.CYAN + f"URL: {url_found}" + Style.RESET_ALL)
                            else:
                                print(Fore.YELLOW + f"[?] URL not found for {filename}" + Style.RESET_ALL)
                            print(Fore.GREEN + f"\n--- {filename} ---\n" + Style.RESET_ALL)
                            try:
                                with open(js_path, 'r', encoding='utf-8', errors='replace') as f:
                                    content = f.read()
                                    print(highlight_js_comments(content))
                            except Exception as e:
                                print(Fore.RED + f"[!] Could not read {filename}: {e}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No JS directory found.' + Style.RESET_ALL)
                elif sub_cmd.strip() == 'extras':
                    extras_dir = os.path.join(os.getcwd(), 'enu', 'web', 'extras')
                    if os.path.isdir(extras_dir):
                        files = sorted(os.listdir(extras_dir))
                        if not files:
                            print(Fore.YELLOW + '[*] No extras files found.' + Style.RESET_ALL)
                        for filename in files:
                            extras_path = os.path.join(extras_dir, filename)
                            print(Fore.GREEN + f"\n--- {filename} ---\n" + Style.RESET_ALL)
                            try:
                                with open(extras_path, 'r', encoding='utf-8', errors='replace') as f:
                                    content = f.read()
                                    # Highlight comments for known types
                                    if filename.endswith('.xml'):
                                        # XML comments <!-- ... -->
                                        content = re.sub(r'(<!--.*?-->)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, content, flags=re.DOTALL)
                                    elif filename.endswith('.txt'):
                                        # robots.txt: lines starting with #
                                        content = re.sub(r'(^#.*$)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, content, flags=re.MULTILINE)
                                    print(content)
                            except Exception as e:
                                print(Fore.RED + f"[!] Could not read {filename}: {e}" + Style.RESET_ALL)
                    else:
                        print(Fore.YELLOW + '[*] No extras directory found.' + Style.RESET_ALL)
                    # HTML
                    html_dir = os.path.join(base_dir, 'html')
                    if os.path.isdir(html_dir):
                        for filename in sorted(os.listdir(html_dir)):
                            html_path = os.path.join(html_dir, filename)
                            print_comments_from_file(html_path, html_pat, filename)
                    # CSS
                    css_dir = os.path.join(base_dir, 'css')
                    if os.path.isdir(css_dir):
                        for filename in sorted(os.listdir(css_dir)):
                            css_path = os.path.join(css_dir, filename)
                            print_comments_from_file(css_path, css_pat, filename)
                    # JS
                    js_dir = os.path.join(base_dir, 'js')
                    if os.path.isdir(js_dir):
                        for filename in sorted(os.listdir(js_dir)):
                            js_path = os.path.join(js_dir, filename)
                            print_comments_from_file(js_path, js_pat1, filename)
                            print_comments_from_file(js_path, js_pat2, filename)
                    # Extras
                    extras_dir = os.path.join(base_dir, 'extras')
                    if os.path.isdir(extras_dir):
                        for filename in sorted(os.listdir(extras_dir)):
                            extras_path = os.path.join(extras_dir, filename)
                            if filename.endswith('.xml'):
                                print_comments_from_file(extras_path, xml_pat, filename)
                            elif filename.endswith('.txt'):
                                print_comments_from_file(extras_path, txt_pat, filename)
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
        print(Fore.GREEN + '  http_head       - HTTP HEAD request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  spider          - Crawl links from the set url and save files' + Style.RESET_ALL)
        print(Fore.GREEN + '  html            - Show all HTML files found, with URLs and highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  css             - Show all CSS files found, with URLs and highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  js              - Show all JS files found, with URLs and highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  extras          - Show all extra files (robots.txt, sitemap.xml, etc) with highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  comments         - Show all comments from HTML, CSS, JS, and extras files' + Style.RESET_ALL)
        print(Fore.GREEN + '  set <opt> <val> - Set an option (url, domain)' + Style.RESET_ALL)
        print(Fore.GREEN + '  options         - Show current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  clear           - Clear the terminal' + Style.RESET_ALL)
        print(Fore.GREEN + '  ls, ls -la      - List files in the current directory' + Style.RESET_ALL)
        print(Fore.GREEN + '  cat <file>      - Show contents of a file' + Style.RESET_ALL)
        print(Fore.GREEN + '  tree            - Show directory tree' + Style.RESET_ALL)
        print(Fore.GREEN + '  !<cmd>          - Run any system command (e.g. !whoami)' + Style.RESET_ALL)
        print(Fore.GREEN + '  help/?          - Show this help menu' + Style.RESET_ALL)
        print(Fore.GREEN + '  exit/back       - Return to main console' + Style.RESET_ALL)

    def complete(self, text, line, begidx, endidx):
        cmds = ['http_get', 'http_post', 'http_head', 'spider', 'set', 'options', 'clear', 'help', '?', 'exit', 'back']
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
