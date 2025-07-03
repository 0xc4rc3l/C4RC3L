# C4RC3L Pentesting Framework

C4RC3L is a modular, Metasploit-like pentesting framework written in Python, designed for workflow-driven penetration testing with a robust, user-friendly console interface.

## Features

- **Console Interface**: Colorful, msfconsole-inspired prompt with random ASCII art banners at startup.
- **Robust Ctrl+C Handling**: All prompts and modules handle Ctrl+C gracefully.
- **Global Options**: Set and persist global options (`target`, `url`, `domain`, `dir_list`, `sub_list`, `file_list`) with validation and autocomplete.
- **Module System**: Modular design with a portscan module and web module entry point. Easy to extend.
- **System Command Support**: Run common Linux commands (`ls`, `cd`, `cat`, `git`, `searchsploit`, etc.) from any prompt, with tab-completion for files/dirs. Output is shown exactly as in a shell, with no extra error messages.
- **Workspace & Workflow**:
  - Workflow directories (`enu`, `files`, `exploits`, `loot`) are always in the project root.
  - All logs and persistent state are stored in `logs/workspace`.
  - `init` command sets up the correct directory structure and cleans up any misplaced workflow dirs.
  - `workspace` command shows workspace status and path.
- **Persistence**: Global options and portscan results are saved in `logs/workspace/c4rc3l_state.json`.
- **Portscan Module**:
  - TCP/UDP port scanning using nmap.
  - Service/script scan on open ports.
  - Save service scan results in all nmap formats to `enu/` with `service {name}`.
  - View last open ports with `ports`.
- **Web Module**: Entry point for future web exploitation modules, with its own prompt and options.
- **Help System**: `help` command lists all commands and explains workspace/workflow usage.
- **Autocomplete**: Tab-completion for global options and system command file/dir arguments.

## Usage

1. **Initialize Workflow**
   ```
   init
   ```
   This creates `enu`, `files`, `exploits`, `loot` in the project root and `logs/workspace` for logs/state.

2. **Set Global Options**
   ```
   set target 192.168.1.1
   set url http://example.com
   set domain example.com
   ```
   Use tab for option autocomplete.

3. **Run System Commands**
   ```
   ls
   cd enu
   git status
   searchsploit windows smb
   ```
   Tab-completion works for file/dir arguments. Output is shown as in a normal shell.

4. **Portscan Module**
   ```
   portscan
   set target 192.168.1.1
   scan
   ports
   service myscan
   exit
   ```
   - `scan` runs a port scan.
   - `service {name}` runs a service/script scan and saves results as `enu/{name}.nmap/.xml/.gnmap`.

5. **Web Module**
   ```
   web
   set url http://example.com
   options
   exit
   ```

6. **Workspace Management**
   ```
   workspace
   ```
   Shows the current workspace path and status.

## Directory Structure

- `enu/`, `files/`, `exploits/`, `loot/` — workflow directories in project root
- `logs/workspace/` — all logs and persistent state
- `logs/workspace/c4rc3l_state.json` — global options and portscan results

## Extending
- Add new modules in the `modules/` directory and integrate via the main console.
- System command support is easily extensible by adding to the `allowed` list.

## Requirements
- Python 3.7+
- `colorama` (for colored output)
- `nmap` (for port scanning)
- `searchsploit` (optional, for exploit-db integration)

## Author
- Developed by 0xc4rc3l

---

For more details, see the code and use the `help` command in the console.
