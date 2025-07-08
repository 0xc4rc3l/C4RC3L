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
        # Initialize user_creds as an empty list
        self.user_creds = []

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
                    login_pages = []
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
                                        # If robots.txt, parse for directories and add to to_visit
                                        if fname == 'robots.txt':
                                            try:
                                                lines = resp.text.splitlines()
                                                for line in lines:
                                                    line = line.strip()
                                                    if line.lower().startswith('disallow:') or line.lower().startswith('allow:'):
                                                        path = line.split(':', 1)[1].strip()
                                                        if path and path != '/':
                                                            # Append to front of set url
                                                            full_url = urljoin(url, path)
                                                            if full_url not in to_visit and full_url not in visited:
                                                                to_visit.append(full_url)
                                            except Exception as e:
                                                print(Fore.RED + f"[!] Failed to parse robots.txt: {e}" + Style.RESET_ALL)
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
                                    # Detect login page
                                    try:
                                        soup = BeautifulSoup(resp.text, 'html.parser')
                                        # Check URL for login keywords
                                        login_keywords = ['login', 'signin', 'auth', 'password']
                                        url_lower = current.lower()
                                        if any(kw in url_lower for kw in login_keywords):
                                            login_pages.append(current)
                                        # Check forms for login fields
                                        for form in soup.find_all('form'):
                                            action = form.get('action', '').lower()
                                            if any(kw in action for kw in login_keywords):
                                                login_pages.append(current)
                                                break
                                            for inp in form.find_all('input'):
                                                name = inp.get('name', '').lower()
                                                id_ = inp.get('id', '').lower()
                                                typ = inp.get('type', '').lower()
                                                if any(kw in name for kw in login_keywords) or any(kw in id_ for kw in login_keywords) or typ == 'password':
                                                    login_pages.append(current)
                                                    break
                                    except Exception:
                                        pass
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
                                    try:
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
                                    except Exception:
                                        pass
                    except Exception as e:
                        print(Fore.RED + f"[!] Spider failed: {e}" + Style.RESET_ALL)
                    print(Fore.GREEN + f"[+] Spider complete. {len(found_links)} links written to enu/spider.txt" + Style.RESET_ALL)
                    if login_pages:
                        print(Fore.MAGENTA + f"[!] Possible login page(s) found:" + Style.RESET_ALL)
                        for lp in set(login_pages):
                            print(Fore.MAGENTA + f"    {lp}" + Style.RESET_ALL)
                        # Use default credentials list
                        default_creds = [
                            ('admin', 'admin'),
                            ('admin', 'password'),
                            ('root', 'root'),
                            ('user', 'user'),
                            ('test', 'test'),
                            ('administrator', 'admin'),
                            ('admin', '1234'),
                            ('admin', '12345'),
                            ('admin', '123456'),
                            ('admin', ''),
                            ('', 'admin'),
                        ]
                        # Add user-supplied creds if any
                        if self.user_creds:
                            default_creds = self.user_creds + default_creds
                        for login_url in set(login_pages):
                            try:
                                resp = requests.get(login_url, timeout=10)
                                soup = BeautifulSoup(resp.text, 'html.parser')
                                for form in soup.find_all('form'):
                                    action = form.get('action')
                                    method = form.get('method', 'post').lower()
                                    form_url = urljoin(login_url, action) if action else login_url
                                    payload = {}
                                    user_field = pass_field = None
                                    # Try to detect username and password fields
                                    for inp in form.find_all('input'):
                                        name = inp.get('name')
                                        typ = inp.get('type', '').lower()
                                        if not name:
                                            continue
                                        if typ == 'password' or 'pass' in name.lower():
                                            pass_field = name
                                        elif typ in ('text', 'email') or 'user' in name.lower() or 'email' in name.lower():
                                            user_field = name
                                    if user_field and pass_field:
                                        for username, password in default_creds:
                                            test_payload = {}
                                            for inp in form.find_all('input'):
                                                name = inp.get('name')
                                                typ = inp.get('type', '').lower()
                                                if not name:
                                                    continue
                                                if name == user_field:
                                                    test_payload[name] = username
                                                elif name == pass_field:
                                                    test_payload[name] = password
                                                else:
                                                    test_payload[name] = inp.get('value', '')
                                            print(Fore.YELLOW + f"[*] Trying {username}:{password} on {form_url}..." + Style.RESET_ALL)
                                            try:
                                                resp = requests.post(form_url, data=test_payload, timeout=10, allow_redirects=False)
                                                # Check for redirect
                                                if resp.is_redirect or resp.is_permanent_redirect or resp.status_code in (301, 302, 303, 307, 308):
                                                    location = resp.headers.get('Location')
                                                    print(Fore.CYAN + f"[!] Login attempt to {form_url} with {username}:{password} resulted in a redirect to: {location}" + Style.RESET_ALL)
                                                    # Follow the redirect
                                                    if location:
                                                        redirect_url = urljoin(form_url, location)
                                                        try:
                                                            redirect_resp = requests.get(redirect_url, timeout=10)
                                                            print(Fore.YELLOW + '[*] Redirect Response Headers:' + Style.RESET_ALL)
                                                            for k, v in redirect_resp.headers.items():
                                                                print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                                                            if redirect_resp.cookies:
                                                                print(Fore.YELLOW + '[*] Redirect Cookies:' + Style.RESET_ALL)
                                                                for c in redirect_resp.cookies:
                                                                    print(Fore.WHITE + f"  {c.name}={c.value}" + Style.RESET_ALL)
                                                        except Exception as e:
                                                            print(Fore.RED + f"[!] Error following redirect: {e}" + Style.RESET_ALL)
                                                    # Also show cookies set in the redirect response
                                                    if resp.cookies:
                                                        print(Fore.YELLOW + '[*] Cookies set on redirect:' + Style.RESET_ALL)
                                                        for c in resp.cookies:
                                                            print(Fore.WHITE + f"  {c.name}={c.value}" + Style.RESET_ALL)
                                                    break
                                                elif resp.status_code == 200 and not re.search(r'fail|invalid|error|incorrect', resp.text, re.I):
                                                    print(Fore.GREEN + f"[+] Login attempt to {form_url} with {username}:{password} may have succeeded!" + Style.RESET_ALL)
                                                    # Display response headers
                                                    print(Fore.YELLOW + '[*] Response Headers:' + Style.RESET_ALL)
                                                    for k, v in resp.headers.items():
                                                        print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                                                    # Display cookies
                                                    if resp.cookies:
                                                        print(Fore.YELLOW + '[*] Cookies:' + Style.RESET_ALL)
                                                        for c in resp.cookies:
                                                            print(Fore.WHITE + f"  {c.name}={c.value}" + Style.RESET_ALL)
                                                    break
                                                else:
                                                    print(Fore.RED + f"[-] Login attempt to {form_url} with {username}:{password} failed or uncertain." + Style.RESET_ALL)
                                            except Exception as e:
                                                print(Fore.RED + f"[!] Login request error: {e}" + Style.RESET_ALL)
                                    else:
                                        print(Fore.YELLOW + f"[!] Could not determine username/password fields for {form_url}" + Style.RESET_ALL)
                            except Exception as e:
                                print(Fore.RED + f"[!] Could not test login for {login_url}: {e}" + Style.RESET_ALL)
                elif sub_cmd == 'login':
                    url = self.options.get('url') or self.global_options.get('url')
                    if not url:
                        print(Fore.RED + '[!] Set url first: set url <url>' + Style.RESET_ALL)
                        return
                    from urllib.parse import urljoin
                    from bs4 import BeautifulSoup
                    # Try login on the set url with user_creds only
                    if not self.user_creds:
                        print(Fore.YELLOW + '[*] No user credentials added. Use add_creds <user> <pass> first.' + Style.RESET_ALL)
                        return
                    try:
                        resp = requests.get(url, timeout=10)
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        found_form = False
                        for form in soup.find_all('form'):
                            action = form.get('action')
                            method = form.get('method', 'post').lower()
                            form_url = urljoin(url, action) if action else url
                            user_field = pass_field = None
                            for inp in form.find_all('input'):
                                name = inp.get('name')
                                typ = inp.get('type', '').lower()
                                if not name:
                                    continue
                                if typ == 'password' or 'pass' in name.lower():
                                    pass_field = name
                                elif typ in ('text', 'email') or 'user' in name.lower() or 'email' in name.lower():
                                    user_field = name
                            if user_field and pass_field:
                                found_form = True
                                for username, password in self.user_creds:
                                    test_payload = {}
                                    for inp in form.find_all('input'):
                                        name = inp.get('name')
                                        typ = inp.get('type', '').lower()
                                        if not name:
                                            continue
                                        if name == user_field:
                                            test_payload[name] = username
                                        elif name == pass_field:
                                            test_payload[name] = password
                                        else:
                                            test_payload[name] = inp.get('value', '')
                                    print(Fore.YELLOW + f"[*] Trying {username}:{password} on {form_url}..." + Style.RESET_ALL)
                                    try:
                                        if method == 'post':
                                            login_resp = requests.post(form_url, data=test_payload, timeout=10, allow_redirects=False)
                                        else:
                                            login_resp = requests.get(form_url, params=test_payload, timeout=10, allow_redirects=False)
                                        print(Fore.CYAN + f"[Status] HTTP {login_resp.status_code}" + Style.RESET_ALL)
                                        if login_resp.is_redirect or login_resp.is_permanent_redirect or login_resp.status_code in (301, 302, 303, 307, 308):
                                            location = login_resp.headers.get('Location')
                                            print(Fore.CYAN + f"[!] Login attempt to {form_url} with {username}:{password} resulted in a redirect to: {location}" + Style.RESET_ALL)
                                            if location:
                                                redirect_url = urljoin(form_url, location)
                                                try:
                                                    redirect_resp = requests.get(redirect_url, timeout=10)
                                                    print(Fore.YELLOW + '[*] Redirect Response Headers:' + Style.RESET_ALL)
                                                    for k, v in redirect_resp.headers.items():
                                                        print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                                                    if redirect_resp.cookies:
                                                        print(Fore.YELLOW + '[*] Redirect Cookies:' + Style.RESET_ALL)
                                                        for c in redirect_resp.cookies:
                                                            print(Fore.WHITE + f"  {c.name}={c.value}" + Style.RESET_ALL)
                                                except Exception as e:
                                                    print(Fore.RED + f"[!] Error following redirect: {e}" + Style.RESET_ALL)
                                            if login_resp.cookies:
                                                print(Fore.YELLOW + '[*] Cookies set on redirect:' + Style.RESET_ALL)
                                                for c in login_resp.cookies:
                                                    print(Fore.WHITE + f"  {c.name}={c.value}" + Style.RESET_ALL)
                                            break
                                        elif login_resp.status_code == 200 and not re.search(r'fail|invalid|error|incorrect', login_resp.text, re.I):
                                            print(Fore.GREEN + f"[+] Login attempt to {form_url} with {username}:{password} may have succeeded!" + Style.RESET_ALL)
                                            print(Fore.YELLOW + '[*] Response Headers:' + Style.RESET_ALL)
                                            for k, v in login_resp.headers.items():
                                                print(Fore.WHITE + f"  {k}: {v}" + Style.RESET_ALL)
                                            if login_resp.cookies:
                                                print(Fore.YELLOW + '[*] Cookies:' + Style.RESET_ALL)
                                                for c in login_resp.cookies:
                                                    print(Fore.WHITE + f"  {c.name}={c.value}" + Style.RESET_ALL)
                                            break
                                        else:
                                            print(Fore.RED + f"[-] Login attempt to {form_url} with {username}:{password} failed or uncertain." + Style.RESET_ALL)
                                    except Exception as e:
                                        print(Fore.RED + f"[!] Login request error: {e}" + Style.RESET_ALL)
                                break
                        if not found_form:
                            print(Fore.YELLOW + '[*] No login form found on the page.' + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[!] Could not test login for {url}: {e}" + Style.RESET_ALL)
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
                        # Highlight HTML comments
                        text = re.sub(r'(<!--.*?-->)', lambda m: Fore.MAGENTA + m.group(1) + Style.RESET_ALL, text, flags=re.DOTALL)
                        # Highlight <script>...</script> blocks
                        text = re.sub(r'(<script.*?>.*?</script>)', lambda m: Fore.YELLOW + m.group(1) + Style.RESET_ALL, text, flags=re.DOTALL|re.IGNORECASE)
                        return text
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
                elif sub_cmd.strip() == 'comments':
                    base_dir = os.path.join(os.getcwd(), 'enu', 'web')
                    found_any = False
                    def print_comments_from_file(filepath, pattern, filename):
                        nonlocal found_any
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                                content = f.read()
                                matches = re.findall(pattern, content, flags=re.DOTALL | re.MULTILINE)
                                if matches:
                                    found_any = True
                                    print(Fore.GREEN + f"\n--- {filename} ---\n" + Style.RESET_ALL)
                                    for m in matches:
                                        print(Fore.MAGENTA + m.strip() + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + f"[!] Could not read {filename}: {e}" + Style.RESET_ALL)
                    # Patterns
                    html_pat = r'<!--.*?-->'
                    css_pat = r'/\*.*?\*/'
                    js_pat1 = r'/\*.*?\*/'
                    js_pat2 = r'//.*?$'
                    xml_pat = r'<!--.*?-->'
                    txt_pat = r'(^#.*$)'
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
                    if not found_any:
                        print(Fore.YELLOW + '[*] No comments found.' + Style.RESET_ALL)
                elif sub_cmd.startswith('add_creds '):
                    parts = sub_cmd.split(maxsplit=2)
                    if len(parts) != 3:
                        print(Fore.RED + 'Usage: add_creds <user> <pass>' + Style.RESET_ALL)
                        continue
                    user, passwd = parts[1], parts[2]
                    self.user_creds.insert(0, (user, passwd))
                    print(Fore.GREEN + f"[+] Added credentials: {user}:{passwd}" + Style.RESET_ALL)
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
        print(Fore.GREEN + '  http_get' + Style.RESET_ALL + Fore.WHITE + '        - HTTP GET request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  http_post' + Style.RESET_ALL + Fore.WHITE + '       - HTTP POST request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  http_head' + Style.RESET_ALL + Fore.WHITE + '       - HTTP HEAD request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  http_options' + Style.RESET_ALL + Fore.WHITE + '    - HTTP OPTIONS request to the set url' + Style.RESET_ALL)
        print(Fore.GREEN + '  spider' + Style.RESET_ALL + Fore.WHITE + '          - Crawl links from the set url and save files' + Style.RESET_ALL)
        print(Fore.GREEN + '  html' + Style.RESET_ALL + Fore.WHITE + '            - Show all HTML files found, with URLs and highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  css' + Style.RESET_ALL + Fore.WHITE + '             - Show all CSS files found, with URLs and highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  js' + Style.RESET_ALL + Fore.WHITE + '              - Show all JS files found, with URLs and highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  extras' + Style.RESET_ALL + Fore.WHITE + '          - Show all extra files (robots.txt, sitemap.xml, etc) with highlighted comments' + Style.RESET_ALL)
        print(Fore.GREEN + '  comments' + Style.RESET_ALL + Fore.WHITE + '        - Show all comments from HTML, CSS, JS, and extras files' + Style.RESET_ALL)
        print(Fore.GREEN + '  set <opt> <val>' + Style.RESET_ALL + Fore.WHITE + ' - Set an option (url, domain)' + Style.RESET_ALL)
        print(Fore.GREEN + '  options' + Style.RESET_ALL + Fore.WHITE + '         - Show current options' + Style.RESET_ALL)
        print(Fore.GREEN + '  clear' + Style.RESET_ALL + Fore.WHITE + '           - Clear the terminal' + Style.RESET_ALL)
        print(Fore.GREEN + '  ls, ls -la' + Style.RESET_ALL + Fore.WHITE + '      - List files in the current directory' + Style.RESET_ALL)
        print(Fore.GREEN + '  cat <file>' + Style.RESET_ALL + Fore.WHITE + '      - Show contents of a file' + Style.RESET_ALL)
        print(Fore.GREEN + '  tree' + Style.RESET_ALL + Fore.WHITE + '           - Show directory tree' + Style.RESET_ALL)
        print(Fore.GREEN + '  !<cmd>' + Style.RESET_ALL + Fore.WHITE + '          - Run any system command (e.g. !whoami)' + Style.RESET_ALL)
        print(Fore.GREEN + '  exit/back' + Style.RESET_ALL + Fore.WHITE + '       - Return to main console' + Style.RESET_ALL)
        print(Fore.GREEN + '  login' + Style.RESET_ALL + Fore.WHITE + '            - Attempt login with only added credentials' + Style.RESET_ALL)

    def complete(self, text, line, begidx, endidx):
        cmds = [
            'http_get', 'http_post', 'http_head', 'http_options', 'spider', 'set', 'options', 'clear',
            'help', '?', 'exit', 'back', 'ls', 'ls -la', 'cat', 'tree', 'html', 'css', 'js', 'extras', 'comments', 'add_creds', 'login'
        ]
        # Tab complete for command
        if begidx == 0:
            return [c for c in cmds if c.startswith(text)]
        # Tab complete for set command options
        if line.strip().startswith('set '):
            opts = [k for k in self.options.keys() if k.startswith(text)]
            return opts
        # Tab complete for cat command (filenames in current dir)
        if line.strip().startswith('cat '):
            try:
                files = os.listdir('.')
                return [f for f in files if f.startswith(text)]
            except Exception:
                return []
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
