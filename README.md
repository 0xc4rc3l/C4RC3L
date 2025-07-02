# C4RC3L - Python Pentesting Framework

C4RC3L is a modular, Metasploit-like penetration testing framework written in Python. It features a colorful console interface, module system, and global option management, designed to mimic the workflow and experience of `msfconsole`.

## Features

- **Colorful Console**: Random ASCII art banners and colorized prompts for a modern, hacker-friendly look.
- **Modular Architecture**: Easily add new modules (e.g., port scanning, brute-force, exploits, etc.).
- **Global Options**: Manage `target`, `url`, and `domain` globally, with validation and normalization.
- **Module-Specific Prompts**: Each module has its own sub-console and commands.
- **Autocomplete & Help**: Tab-completion and horizontal help menus for commands and options.
- **Port Scanner Module**: Built-in TCP/UDP port scanner as a starting module, using nmap.
- **Clear Command**: Available in all modules and the main console.

## Getting Started

### Requirements
- Python 3.7+
- [colorama](https://pypi.org/project/colorama/)
- [nmap](https://nmap.org/) (for port scanning module)

Install dependencies:
```bash
pip install colorama
```

### Usage
Run the main console:
```bash
python3 C4RC3L.py
```

### Main Commands
- `set <option> <value>`: Set a global option (`target`, `url`, `domain`).
- `show`: Show current global options.
- `portscan`: Enter the port scanner module.
- `clear`: Clear the terminal.
- `exit`: Exit the framework.
- `help` or `?`: Show help menu.

### Portscan Module
- `scan`: Run a port scan with current options.
- `set <option> <value>`: Set module option (`target`, `type`).
- `options`: Show current module options.
- `clear`: Clear the terminal.
- `exit`/`back`: Return to main console.

## Example Workflow
```
C4RC3L > set target 192.168.1.1
C4RC3L > set url example.com
C4RC3L > set domain example.com
C4RC3L > portscan
C4RC3L [portscan] > set type udp
C4RC3L [portscan] > scan
```

## Notes
- The welcome message and banner are only shown once at startup.
- Pressing Ctrl+C in the main console or any module will never exit the program or stack prompts; it simply returns to the current prompt.
- To exit, type `exit` in the main console.

## Adding Modules
1. Create a new Python file in `modules/` (e.g., `modules/bruteforce.py`).
2. Implement your module logic and expose a function (e.g., `run_bruteforce`).
3. Integrate the module in `C4RC3L.py` with its own sub-console and options.

## Roadmap
- More modules (exploit, brute-force, auxiliary, post-exploitation, etc.)
- Persistent storage for options
- Advanced scanning (nmap integration, threading)
- Logging and error handling

## License
MIT

---
Developed by [0xc4rc3l](https://github.com/0xc4rc3l)
