# C4RC3L Web Module

## Features

- **HTTP Requests**: Perform GET, POST, HEAD, and OPTIONS requests to the set URL. View status codes, headers, and response bodies.
- **Spidering**: Crawl the set URL, parse `robots.txt` for directories, and recursively download HTML, CSS, JS, and extra files. Detects possible login pages and attempts logins with default and user-supplied credentials.
- **Login Automation**: Detects login forms and attempts login using a prioritized list of credentials. Shows HTTP status code, headers, cookies, and redirect information for each attempt.
- **Credential Management**: Add your own credentials with `add_creds <user> <pass>`. These are prioritized in login attempts and used by the `login` command.
- **Comment Extraction**: Extract and highlight comments from HTML, CSS, JS, and extra files (e.g., `robots.txt`, `sitemap.xml`).
- **File Browsing**: View all downloaded HTML, CSS, JS, and extra files with syntax highlighting for comments and scripts.
- **Tab Completion**: Tab-complete all commands, options, and filenames for the `cat` command.
- **User Experience**: Colorful output, improved help menu, and system command passthrough.

## Commands

- `set <option> <value>`: Set an option (`url`, `domain`).
- `options`: Show current options.
- `http_get`, `http_post`, `http_head`, `http_options`: Make HTTP requests to the set URL.
- `spider`: Crawl the set URL, save files, detect login pages, and attempt logins.
- `login`: Attempt login on the set URL using only user-added credentials.
- `add_creds <user> <pass>`: Add credentials for login attempts (prioritized over defaults).
- `html`, `css`, `js`, `extras`: Show all downloaded files of each type, with URLs and highlighted comments.
- `comments`: Show all comments from HTML, CSS, JS, and extras files.
- `ls`, `ls -la`, `cat <file>`, `tree`: File system commands.
- `!<cmd>`: Run any system command (e.g., `!whoami`).
- `clear`: Clear the terminal.
- `help`, `?`: Show help menu.
- `exit`, `back`: Return to main console.

## Usage Notes

- Set the target URL first: `set url http://example.com`
- Use `spider` to crawl and enumerate files and login forms.
- Use `add_creds <user> <pass>` to add your own credentials for login attempts.
- Use `login` to attempt login with only your added credentials.
- All login attempts display the HTTP status code for transparency.

## Requirements

- Python 3.7+
- `requests`, `colorama`, `readline`, `bs4` (BeautifulSoup4)

Install dependencies:

```
pip install requests colorama readline beautifulsoup4
```

---

For more details, see the code in `modules/web.py`.
