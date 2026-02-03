# Microsoft Rewards Automator

Automated bot for earning Microsoft Rewards points through Bing searches with a simple GUI interface.

## Features

### ✅ Implemented
- **Search Mode**: Automated Bing searches with configurable loops
- **Human-like Behavior**: Random delays between actions (2-7 seconds) to mimic natural user behavior
- **Multi-layer Automation**: 
  - Primary: Selenium-based DOM control for reliability
  - Fallback 1: OS-level keyboard events (pynput)
  - Fallback 2: GUI automation (pyautogui)
- **GUI Interface**: Clean, intuitive Tkinter interface with two independent operation modes
- **Automatic Driver Management**: webdriver-manager auto-downloads Edge driver
- **Search Term Variety**: Loads search terms from `wordlist.txt` or `apache.txt`
- **10-Second Wait**: Mandatory wait after each search to ensure points registration

### 🚧 Coming Soon (WIP)
- **Task Helper**: Task detection and completion assistance
  - Will identify available tasks on Microsoft Rewards dashboard
  - Provide guided completion of daily tasks
  - Auto-detect task status

## Requirements

- **Python 3.7+** (with Tkinter support)
- **Windows** (primary development target)
- Microsoft Edge browser
- Internet connection

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Auto-Microsoft-Rewards.git
cd Auto-Microsoft-Rewards
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- `selenium>=4.0` - Browser automation
- `webdriver-manager>=3.8` - Automatic driver management

**Optional packages:**
- `pyautogui` - GUI automation fallback
- `pynput` - OS-level keyboard control
- `pygetwindow` - Window positioning

## Usage

### GUI Mode (Default)
```bash
python RewardsFarmer.py
```

This launches the graphical interface with two independent panels:

#### Search Mode
- Set number of loops (1-100)
- Click "Start Search"
- Script will:
  1. Open Edge
  2. Perform Bing search with random term
  3. Wait 10 seconds for points to register
  4. Close Edge
  5. Repeat for each loop with human-like delays

#### Task Helper (WIP)
- Currently loads Microsoft Rewards dashboard
- Edge remains open for manual task completion
- Full automation coming soon

### Search Terms

Place search terms in one of these files (one per line):
- `wordlist.txt` (checked first)
- `apache.txt` (fallback)

Example:
```
artificial intelligence
machine learning
python programming
web development
```

## How It Works

### Search Automation Flow
1. **Pre-launch delay**: 2-5 seconds (human thinking time)
2. **Launch Edge**: Multiple fallback methods for reliability
3. **Window load**: 2-4 seconds (page render time)
4. **Pre-type delay**: 0.5-1.5 seconds (user reading time)
5. **Perform search**: Selenium DOM control or keyboard simulation
6. **Points wait**: 10 seconds (mandatory for point registration)
7. **Pre-close delay**: 1-3 seconds (user behavior)
8. **Close Edge**: Taskkill force-close
9. **Between-loop delay**: 3-7 seconds (natural spacing)

### Fallback Chain
- **Selenium**: DOM-based search (most reliable)
  - Finds search input by name or ID
  - Types directly into element
  - Submits with keyboard event
- **pynput**: OS-level keyboard events
  - Ctrl+L to focus omnibox
  - Character-by-character typing
  - Enter key submission
- **pyautogui**: GUI automation
  - Mouse movement and clicks
  - Keyboard input simulation

## Configuration

### Adjustable Parameters

Edit `RewardsFarmer.py` to customize:
- Delay ranges (lines 155-220)
- Search term files (lines 105-135)
- Window size (line 525: `geometry('700x300')`)
- Loop defaults (line 548, 549)

## Disclaimer

⚠️ **Use at your own risk.** This script automates Microsoft Rewards participation, which may violate Microsoft's Terms of Service. 

**Important notes:**
- Use only on accounts you own
- Microsoft may suspend or ban accounts detected using automation
- This project is for educational purposes
- Author assumes no liability for account restrictions or bans

## Roadmap

### Version 1.0 (Current)
- ✅ Search automation with GUI
- ✅ Human-like behavior patterns
- ✅ Fallback automation methods
- 🚧 Task helper (loading page, staying open for manual completion)

### Version 1.1 (Planned)
- 🔲 Task auto-detection
- 🔲 Task completion assistance
- 🔲 Daily streak tracking
- 🔲 Reward redemption suggestions

### Version 2.0 (Future)
- 🔲 Advanced task automation
- 🔲 Browser profile management
- 🔲 Cross-platform support (macOS, Linux)
- 🔲 Docker containerization

## Troubleshooting

### Script doesn't find search terms
- Ensure `wordlist.txt` or `apache.txt` exists in script directory
- File must have one search term per line
- Script will use default terms if files not found

### Selenium driver fails
- `webdriver-manager` auto-downloads Edge driver
- Ensure Edge browser is installed
- Delete `~/.wdm/` folder to force re-download

### Keyboard input not working
- Ensure target window has focus
- Try running as Administrator
- Check pyautogui/pynput installation: `pip install --upgrade pynput pyautogui`

### Edge won't launch
- Check if Edge is installed: `msedge.exe` should exist
- Try running script as Administrator
- Verify Windows version (Windows 10+)

## Contributing

Contributions welcome! Areas for help:
- Task automation implementation
- Additional browser support
- Configuration file system
- Better error handling
- Performance optimization

## License

MIT License - See LICENSE file for details

## Disclaimer

This project is not affiliated with Microsoft. Microsoft Rewards is a trademark of Microsoft Corporation. Use this tool at your own discretion and risk.

---

**Last Updated**: February 2026  
**Status**: Side Project
**Author**: CT-OSS
