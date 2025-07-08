# C4RC3L Framework

C4RC3L is a modular, extensible Python framework for penetration testing, web reconnaissance, and security automation. It provides a unified command-line interface and a collection of modules for automating common security tasks, information gathering, and exploitation.

## Project Structure

- `C4RC3L.py` — Main entry point and interactive console.
- `modules/` — Collection of modules for different tasks:
  - `web.py` — Web reconnaissance, spidering, login automation, and more.
  - `portscan.py` — Port scanning and network enumeration.
  - (Add your own modules here for extensibility)

## Key Features

- Modular design: Easily add or extend modules for new tasks.
- Interactive shell: Tab completion, colorized output, and help menus.
- System command passthrough: Run shell commands directly from the console.
- Persistent options: Set and use global or module-specific options.

## Example Modules

### Web Module (`modules/web.py`)

- HTTP requests (GET, POST, HEAD, OPTIONS) with status, headers, and body preview.
- Spidering: Crawl target, parse `robots.txt`, download files, detect login pages.
- Login automation: Detect forms, try default/user credentials, show HTTP status, headers, cookies, and redirects.
- Credential management: Add credentials with `add_creds <user> <pass>`, prioritized in login attempts.
- Comment extraction: Extract and highlight comments from HTML, CSS, JS, and extras.
- File browsing: View downloaded files with syntax highlighting.
- Tab completion for commands, options, and filenames.

### Portscan Module (`modules/portscan.py`)

- Fast TCP/UDP port scanning.
- Service detection and banner grabbing.
- Output results in colorized, easy-to-read format.
- (Extend with your own scanning or enumeration logic.)

## Usage

1. Start the framework:
   ```
   python3 C4RC3L.py
   ```
2. Use the interactive shell to select and run modules:
   - `web` — Enter the web module.
   - `portscan` — Enter the port scanning module.
   - Use `help` in any module for available commands.
3. Set options as needed (e.g., `set url http://target/`).
4. Run module commands (e.g., `spider`, `add_creds`, `login`, `scan`, etc).
5. Use `exit` or `back` to return to the main console.

## Requirements

- Python 3.7+
- `requests`, `colorama`, `readline`, `bs4` (BeautifulSoup4)

Install dependencies:

```
pip install requests colorama readline beautifulsoup4
```

---

For more details, see the code in `modules/` and the main console in `C4RC3L.py`.
