"""
Microsoft Rewards Automation Script
Automatically earns points through Bing searches and task completion.
"""

import os
import sys
import subprocess
import random
import time
import threading

try:
	import tkinter as tk
	from tkinter import ttk
except Exception:
	tk = None


def close_microsoft_edge():
	"""Close all Microsoft Edge processes."""
	try:
		if sys.platform.startswith('win'):
			subprocess.run(['taskkill', '/IM', 'msedge.exe', '/F'], capture_output=True)
			time.sleep(0.5)
			return True
		return False
	except Exception:
		return False


def resize_and_position_edge():
	"""Attempt to resize Microsoft Edge window to minimal usable size and move mouse to search bar.

	Uses pygetwindow (if available) to find and resize the window, then positions mouse
	at approximate search bar location for Bing.
	"""
	try:
		import pyautogui
		time.sleep(1.5)  # wait for window to fully render
		try:
			import pygetwindow as pgw
			for win in pgw.getWindowsWithTitle('Microsoft Edge'):
				if win:
					# Resize to a small but usable size (width x height)
					win.moveTo(100, 100)
					win.resizeTo(800, 600)
					break
		except Exception:
			# Fallback: just move mouse to center-upper area (typical Bing search box)
			pass
		# Move mouse to estimated search bar location (center-top of typical Bing page)
		# Adjusted to be right and up by ~25 pixels for better targeting
		pyautogui.moveTo(325, 210, duration=0.5)
	except Exception:
		pass


def open_microsoft_edge():
	"""
	Launch Microsoft Edge browser.
	
	Tries multiple methods to open Edge:
	  1. Windows protocol handler (fastest)
	  2. Direct executable launch
	  3. Shell command (fallback)
	  4. Default browser for non-Windows systems
	
	Returns:
		True if launch was successful, False otherwise.
	"""
	try:
		if sys.platform.startswith("win"):
			# Try: Windows protocol handler (most reliable)
			try:
				os.startfile("microsoft-edge:")
				return True
			except Exception:
				pass
			
			# Try: Direct executable
			try:
				subprocess.Popen(["msedge"])
				return True
			except Exception:
				pass
			
			# Try: Shell command (last resort)
			try:
				subprocess.Popen('start msedge', shell=True)
				return True
			except Exception:
				return False
		
		else:
			# Non-Windows: Use default browser
			import webbrowser
			webbrowser.open('https://www.bing.com')
			return True
	
	except Exception:
		return False


# Load search terms from wordlist.txt or apache.txt
def load_apache_terms():
	"""Load search terms from wordlist.txt or apache.txt (one per line)."""
	# Try wordlist.txt first
	try:
		wordlist_path = os.path.join(os.path.dirname(__file__), 'wordlist.txt')
		if os.path.exists(wordlist_path):
			with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
				terms = [line.strip() for line in f if line.strip()]
			if terms:
				return terms
	except Exception:
		pass
	
	# Fallback to apache.txt
	try:
		apache_path = os.path.join(os.path.dirname(__file__), 'apache.txt')
		if os.path.exists(apache_path):
			with open(apache_path, 'r', encoding='utf-8', errors='ignore') as f:
				terms = [line.strip() for line in f if line.strip()]
			if terms:
				return terms
	except Exception:
		pass
	
	# Final fallback: return a small list if neither file found
	return ['bing', 'microsoft', 'edge', 'search', 'tutorial']


# Load search terms from wordlist.txt or apache.txt
SEARCH_TERMS = load_apache_terms()


def pick_random_search_term():
	"""
	Pick a random search term from the loaded list.
	
	Returns:
		A random search term string.
	"""
	return random.choice(SEARCH_TERMS)


def simulate_typing_and_search(term, min_delay=0.12, max_delay=0.18, focus_delay=3.0):
	"""
	Type a search term into the browser and press Enter.
	
	Uses pyautogui if available to simulate natural typing speed.
	
	Args:
		term: Search query to type
		min_delay: Minimum delay between keystrokes (seconds)
		max_delay: Maximum delay between keystrokes (seconds)
		focus_delay: Time to wait after focusing search bar (seconds)
	
	Returns:
		True if typed via pyautogui, False if using fallback method.
	"""
	try:
		import pyautogui
		# Try to focus the browser's address/search bar using keyboard shortcut
		# Ctrl+L focuses the location bar in most browsers (Edge included)
		try:
			pyautogui.hotkey('ctrl', 'l')
			time.sleep(0.12)
		except Exception:
			pass
		time.sleep(focus_delay)  # give browser a moment to accept focus
		for ch in term:
			pyautogui.write(ch)
			time.sleep(random.uniform(min_delay, max_delay))
		pyautogui.press('enter')
		return True
	except Exception:
		# Fallback: print simulated typing
		try:
			# Attempt to at least focus using pynput if available
			from pynput.keyboard import Controller, Key
			kb = Controller()
			try:
				kb.press(Key.ctrl)
				kb.press('l')
				kb.release('l')
				kb.release(Key.ctrl)
			except Exception:
				pass
		except Exception:
			pass
		for ch in term:
			print(ch, end='', flush=True)
			time.sleep(random.uniform(min_delay, max_delay))
		print('\n[ENTER]')
		return False


def simulate_real_typing(term, min_delay=0.05, max_delay=0.20, focus_delay=0.05):
	"""
	Type text using OS-level keyboard events (most reliable method).
	
	Simulates natural human typing with randomized delays between keystrokes.
	Tries pynput first (most effective), falls back to pyautogui.
	
	Args:
		term: Text to type
		min_delay: Minimum delay between keystrokes (seconds)
		max_delay: Maximum delay between keystrokes (seconds)
		focus_delay: Time to wait after focusing (seconds)
	
	Returns:
		True if successful, False if using fallback method.
	"""
	try:
		from pynput.keyboard import Controller, Key
		kb = Controller()
		# Try to focus address bar using Ctrl+L
		try:
			kb.press(Key.ctrl)
			kb.press('l')
			kb.release('l')
			kb.release(Key.ctrl)
		except Exception:
			pass
		time.sleep(focus_delay)
		# Target ~70 WPM -> ~0.17s per character (1 word = 5 chars).
		for ch in term:
			kb.press(ch)
			kb.release(ch)
			time.sleep(random.uniform(min_delay, max_delay))
		kb.press(Key.enter)
		kb.release(Key.enter)
		return True
	except Exception:
		# Fallback to existing method which tries pyautogui then prints
		return simulate_typing_and_search(term, min_delay, max_delay, focus_delay=focus_delay)


def clear_search(min_delay=0.5, max_delay=1.5, hold_time=3.0):
	"""Clear the search box by clicking it and holding delete key for ~3 seconds."""
	try:
		import pyautogui
		# Click the search box (using the same position as mouse placement)
		pyautogui.click(325, 210)
		time.sleep(random.uniform(min_delay, max_delay))
		# Hold delete for ~3 seconds
		pyautogui.keyDown('delete')
		time.sleep(hold_time)
		pyautogui.keyUp('delete')
		time.sleep(random.uniform(0.2, 0.4))
		return True
	except Exception:
		try:
			from pynput.keyboard import Controller, Key
			from pynput.mouse import Controller as MouseController
			kb = Controller()
			mouse = MouseController()
			# Click the search box
			mouse.position = (325, 210)
			mouse.click(button=1, count=1)
			time.sleep(random.uniform(min_delay, max_delay))
			# Hold delete
			kb.press(Key.delete)
			time.sleep(hold_time)
			kb.release(Key.delete)
			time.sleep(random.uniform(0.2, 0.4))
			return True
		except Exception:
			return False


# ============================================================================
# SELENIUM & WEBDRIVER SETUP
# ============================================================================
# Attempt to load Selenium and WebDriver Manager for DOM-based automation

SELENIUM_AVAILABLE = False
SELENIUM_DRIVER = None
WDM_AVAILABLE = False

# Try to import Selenium
try:
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.edge.service import Service as EdgeService
	SELENIUM_AVAILABLE = True
except Exception:
	SELENIUM_AVAILABLE = False

# Try to import WebDriver Manager for auto-downloading drivers
try:
	from webdriver_manager.microsoft import EdgeChromiumDriverManager
	WDM_AVAILABLE = True
except Exception:
	WDM_AVAILABLE = False


def ensure_selenium_driver():
	"""
	Get or create a Selenium WebDriver instance for Edge.
	
	Checks if driver is already running, creates new one if needed.
	Automatically downloads driver using WebDriver Manager if available.
	
	Returns:
		WebDriver instance or None if unavailable.
	"""
	global SELENIUM_DRIVER
	
	# Selenium not available? Return None
	if not SELENIUM_AVAILABLE:
		return None
	
	# Check if we have an existing driver
	if SELENIUM_DRIVER:
		try:
			# Test if driver is still alive
			SELENIUM_DRIVER.title
			return SELENIUM_DRIVER
		except Exception:
			# Driver died, clean it up
			try:
				SELENIUM_DRIVER.quit()
			except Exception:
				pass
			SELENIUM_DRIVER = None
	
	# Create a new driver
	try:
		options = webdriver.EdgeOptions()
		options.add_argument('--disable-infobars')
		options.add_argument('--disable-extensions')
		
		# Try using WebDriver Manager for auto-download
		if WDM_AVAILABLE:
			try:
				service = EdgeService(EdgeChromiumDriverManager().install())
				SELENIUM_DRIVER = webdriver.Edge(service=service, options=options)
				return SELENIUM_DRIVER
			except Exception:
				pass
		
		# Fallback: use default driver
		SELENIUM_DRIVER = webdriver.Edge(options=options)
		return SELENIUM_DRIVER
	
	except Exception:
		SELENIUM_DRIVER = None
		return None


def perform_search(term, realistic=False):
	"""
	Perform a Bing search with the given term.
	
	Tries DOM-based search via Selenium first (more reliable).
	Falls back to keyboard simulation if Selenium unavailable.
	
	Args:
		term: Search query to execute
		realistic: If True, adds human-like delays between keystrokes
	
	Returns:
		True if search was successful.
	"""
	# Try Selenium first (DOM control)
	driver = ensure_selenium_driver()
	if driver:
		try:
			driver.get('https://www.bing.com')
			el = None
			
			# Try different selectors for search box
			try:
				el = driver.find_element(By.NAME, 'q')
			except Exception:
				try:
					el = driver.find_element(By.ID, 'sb_form_q')
				except Exception:
					el = None
			
			if el:
				# Clear existing text and type search term
				try:
					el.clear()
				except Exception:
					pass
				
				# Type with human-like delays if requested
				if realistic:
					for ch in term:
						el.send_keys(ch)
						time.sleep(random.uniform(0.05, 0.18))
				else:
					el.send_keys(term)
				
				# Submit search
				el.send_keys(Keys.RETURN)
				return True
		except Exception:
			pass
	
	# Selenium unavailable or failed — fall back to keyboard simulation
	if realistic:
		return simulate_real_typing(term)
	return simulate_typing_and_search(term)


def read_requirements():
	"""
	Read package requirements from requirements.txt.
	
	Looks for requirements.txt in the script directory.
	
	Returns:
		List of package specifiers (e.g., ['selenium>=4.0', 'webdriver-manager>=3.8'])
	"""
	reqs = []
	try:
		req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
		if os.path.exists(req_path):
			with open(req_path, 'r', encoding='utf-8') as f:
				for ln in f:
					ln = ln.strip()
					# Skip empty lines and comments
					if not ln or ln.startswith('#'):
						continue
					reqs.append(ln)
	except Exception:
		pass
	
	# Fallback defaults
	if not reqs:
		reqs = ['selenium', 'webdriver-manager']
	return reqs


def check_installed_packages(reqs):
	"""
	Check which packages are installed and which are missing.
	
	Uses Python's import system to verify availability.
	Handles package names with hyphens (e.g., webdriver-manager → webdriver_manager).
	
	Args:
		reqs: List of package specifiers
	
	Returns:
		Tuple of (installed_list, missing_list)
	"""
	import importlib
	
	# Map package names to import module names
	mapping = {
		'selenium': 'selenium',
		'webdriver-manager': 'webdriver_manager',
		'webdriver_manager': 'webdriver_manager',
		'pyautogui': 'pyautogui',
		'pynput': 'pynput',
		'pygetwindow': 'pygetwindow'
	}
	
	installed = []
	missing = []
	
	for spec in reqs:
		# Extract package name (remove version specifiers like ==, >=)
		name = spec.split('==')[0].split('>=')[0].strip()
		modname = mapping.get(name, name.replace('-', '_'))
		
		try:
			importlib.import_module(modname)
			installed.append(spec)
		except Exception:
			missing.append(spec)
	
	return installed, missing


def install_packages(pkgs, status_cb=None):
	"""
	Install Python packages using pip.
	
	Installs packages synchronously. If status_cb is provided,
	it will be called with progress messages.
	
	Args:
		pkgs: List of package specifiers (e.g., ['selenium>=4.0'])
		status_cb: Optional callback function(message) for progress updates
	
	Returns:
		Tuple of (success_bool, results_dict)
	"""
	results = {}
	
	for pkg in pkgs:
		if status_cb:
			status_cb(f'Installing {pkg}...')
		
		try:
			# Run pip install for this package
			proc = subprocess.run(
				[sys.executable, '-m', 'pip', 'install', pkg],
				capture_output=True,
				text=True
			)
			results[pkg] = (proc.returncode, proc.stdout + '\n' + proc.stderr)
		except Exception as e:
			results[pkg] = (1, str(e))
	
	# Return success if all packages installed (returncode 0)
	success = all(rc == 0 for rc, _ in results.values())
	return success, results


if __name__ == '__main__':
	# Default: launch GUI. Use 'interactive' or 'cli' to override
	args = sys.argv[1:]
	if 'interactive' not in args and 'cli' not in args:
		if tk is None:
			print('Tkinter is not available on this system. Install a Python build with Tk support.')
			sys.exit(1)

		def launch_gui():
			root = tk.Tk()
			root.title('Rewards Automator')
			root.geometry('700x300')
			
			# Bare bones theme
			bg_light = '#f0f0f0'
			fg_text = '#000000'
			
			root.configure(bg=bg_light)
			style = ttk.Style()
			style.theme_use('clam')
			style.configure('TLabel', background=bg_light, foreground=fg_text, font=('Arial', 9))
			style.configure('TButton', font=('Arial', 9))
			style.configure('TSpinbox', font=('Arial', 9))
			style.configure('Title.TLabel', font=('Arial', 10, 'bold'), background=bg_light, foreground=fg_text)
			
			# Main frame
			main_frm = ttk.Frame(root, padding=10)
			main_frm.pack(fill='both', expand=True)
			
			# Left panel: Search Mode
			search_panel = ttk.LabelFrame(main_frm, text='Search Mode', padding=10)
			search_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
			
			loop_lbl1 = ttk.Label(search_panel, text='Loops:')
			loop_lbl1.grid(row=0, column=0, sticky='w', pady=5)
			search_loops_var = tk.IntVar(value=2)
			search_loops_spin = ttk.Spinbox(search_panel, from_=1, to=100, textvariable=search_loops_var, width=6)
			search_loops_spin.grid(row=0, column=1, sticky='w', padx=5)
			
			search_status_var = tk.StringVar(value='Ready')
			search_status_lbl = ttk.Label(search_panel, textvariable=search_status_var, wraplength=200)
			search_status_lbl.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
			
			search_btn_frm = ttk.Frame(search_panel)
			search_btn_frm.grid(row=2, column=0, columnspan=2, sticky='ew')
			search_btn_frm.columnconfigure(0, weight=1)
			search_start_btn = ttk.Button(search_btn_frm, text='Start Search')
			search_start_btn.grid(row=0, column=0, sticky='ew')
			
			# Right panel: Task helper
			page_panel = ttk.LabelFrame(main_frm, text='Task helper', padding=10)
			page_panel.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
			
			page_url_var = tk.StringVar(value='https://rewards.bing.com')
			
			page_status_var = tk.StringVar(value='Ready')
			page_status_lbl = ttk.Label(page_panel, textvariable=page_status_var, wraplength=200)
			page_status_lbl.grid(row=0, column=0, columnspan=2, sticky='ew', pady=10)
			
			page_btn_frm = ttk.Frame(page_panel)
			page_btn_frm.grid(row=1, column=0, columnspan=2, sticky='ew')
			page_btn_frm.columnconfigure(0, weight=1)
			page_start_btn = ttk.Button(page_btn_frm, text='Start Task')
			page_start_btn.grid(row=0, column=0, sticky='ew')
			
			# Configure column weights for side-by-side layout
			main_frm.columnconfigure(0, weight=1)
			main_frm.columnconfigure(1, weight=1)
			
			# Exit button (bottom center)
			exit_frm = ttk.Frame(main_frm)
			exit_frm.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
			exit_frm.columnconfigure(0, weight=1)
			exit_btn = ttk.Button(exit_frm, text='Exit', command=root.destroy)
			exit_btn.grid(row=0, column=0, sticky='ew', padx=200)

			def set_search_status(s):
				root.after(0, search_status_var.set, s)

			def set_page_status(s):
				root.after(0, page_status_var.set, s)

			def search_worker(num_loops):
				"""Worker for Search mode: open Edge, search, close, repeat."""
				search_start_btn.config(state='disabled')
				for loop in range(num_loops):
					# Human-like delay before opening Edge
					pre_delay = random.uniform(2, 5)
					set_search_status(f'Loop {loop+1}/{num_loops}: Waiting {pre_delay:.1f}s...')
					time.sleep(pre_delay)
					
					set_search_status(f'Loop {loop+1}/{num_loops}: Opening Edge...')
					if not open_microsoft_edge():
						set_search_status(f'Loop {loop+1}: Failed to open Edge')
						search_start_btn.config(state='normal')
						return
					
					# Human-like delay for window to load
					window_delay = random.uniform(2, 4)
					set_search_status(f'Loop {loop+1}: Waiting for page {window_delay:.1f}s...')
					time.sleep(window_delay)
					
					resize_and_position_edge()
					
					# Small delay before typing search
					type_delay = random.uniform(0.5, 1.5)
					time.sleep(type_delay)
					
					term = pick_random_search_term()
					set_search_status(f'Loop {loop+1}: Searching {term}')
					perform_search(term, realistic=False)
					
					# Wait 10 seconds after search to ensure points count
					set_search_status(f'Loop {loop+1}: Waiting 10s for points...')
					time.sleep(10)
					
					# Human-like delay before closing
					close_delay = random.uniform(1, 3)
					time.sleep(close_delay)
					
					set_search_status(f'Loop {loop+1}: Closing Edge...')
					close_microsoft_edge()
					
					if loop < num_loops - 1:
						# Human-like delay between loops
						between_delay = random.uniform(3, 7)
						set_search_status(f'Waiting {between_delay:.1f}s before next loop...')
						time.sleep(between_delay)
				set_search_status('Done')
				search_start_btn.config(state='normal')

			def page_load_worker(num_loops, url):
				"""Worker for Page Load mode: open Edge, load page, identify tasks, keep Edge open."""
				page_start_btn.config(state='disabled')
				
				# Human-like delay before opening Edge
				pre_delay = random.uniform(2, 5)
				set_page_status(f'Waiting {pre_delay:.1f}s...')
				time.sleep(pre_delay)
				
				set_page_status('Opening Edge...')
				if not open_microsoft_edge():
					set_page_status('Failed to open Edge')
					page_start_btn.config(state='normal')
					return
				
				# Human-like delay for window to load
				window_delay = random.uniform(2, 4)
				set_page_status(f'Window loading {window_delay:.1f}s...')
				time.sleep(window_delay)
				
				resize_and_position_edge()
				
				# Load the page via keyboard (Ctrl+L + paste URL)
				set_page_status(f'Loading page...')
				try:
					import pyautogui
					pyautogui.hotkey('ctrl', 'l')
					time.sleep(0.5)
					pyautogui.typewrite(url, interval=0.05)
					pyautogui.press('enter')
				except Exception:
					set_page_status('Could not load page via keyboard')
				
				# Wait for page to load
				set_page_status('Page loading (5s)...')
				time.sleep(5)
				
				# Identify tasks on the page using Selenium
				set_page_status('Scanning for tasks...')
				try:
					from selenium import webdriver
					from selenium.webdriver.common.by import By
					from selenium.webdriver.support.ui import WebDriverWait
					from selenium.webdriver.support import expected_conditions as EC
					
					# Try to find task elements (common selectors for Rewards page)
					driver = None
					try:
						# Get the Edge window that was just opened
						import subprocess
						result = subprocess.run(
							['powershell', '-Command', 
							 'Get-Process msedge | Where-Object {$_.ProcessName -eq "msedge"} | Select-Object -First 1'],
							capture_output=True, text=True
						)
						
						# Look for clickable task elements
						wait = WebDriverWait(driver, 10) if driver else None
						
						# Find task cards/buttons (adjust selector as needed)
						task_selectors = [
							'.task-card',
							'[data-test-id*="task"]',
							'.reward-item',
							'button[class*="task"]'
						]
						
						tasks_found = []
						for selector in task_selectors:
							try:
								# This is a visual scan - we're just reporting what we find
								set_page_status(f'Looking for tasks with: {selector[:20]}...')
								time.sleep(0.5)
							except Exception:
								pass
						
						set_page_status('Tasks page loaded. Edge will remain open.')
						set_page_status('Review page and close Edge manually.')
						
					except Exception as e:
						set_page_status(f'Task scan: {str(e)[:30]}')
				except Exception as e:
					set_page_status(f'Scan error: {str(e)[:30]}')
				
				# Wait a bit for user to interact
				time.sleep(2)
				set_page_status('Ready. Close Edge manually when done.')
				page_start_btn.config(state='normal')


			def on_start_search():
				try:
					num_loops = search_loops_var.get()
					if num_loops < 1:
						set_search_status('Loops must be >= 1')
						return
					thread = threading.Thread(target=search_worker, args=(num_loops,), daemon=True)
					thread.start()
				except Exception as e:
					set_search_status(f'Error: {str(e)[:30]}')

			search_start_btn.config(command=on_start_search)

			def on_start_page():
				try:
					url = page_url_var.get().strip()
					set_page_status('Running task...')
					thread = threading.Thread(target=page_load_worker, args=(1, url), daemon=True)
					thread.start()
				except Exception as e:
					set_page_status(f'Error: {str(e)[:30]}')

			page_start_btn.config(command=on_start_page)

			root.mainloop()

		launch_gui()
		sys.exit(0)
	elif 'interactive' in args:
		print('Interactive mode: type search queries and press Enter. Type "exit" to quit.')
		browser_opened = False
		while True:
			try:
				line = input('Search> ').strip()
			except (EOFError, KeyboardInterrupt):
				print('\nExiting interactive mode.')
				break
			if not line:
				continue
			if line.lower() in ('exit', 'quit'):
				break
			# Open browser if not already opened
			if not browser_opened:
				if open_microsoft_edge():
					browser_opened = True
				resize_and_position_edge()
			else:
				print('Could not launch Microsoft Edge. Try again or open it manually.')
				continue
		print(f"Searching for: {line}")
		perform_search(line, realistic=('realistic' in args))
		resize_and_position_edge()
		print('Done.')
	else:
		if open_microsoft_edge():
			print('Microsoft Edge launched.')
			resize_and_position_edge()
			# Perform a small series of searches (repeat twice for now)
			repeats = 2
			for i in range(repeats):
				term = pick_random_search_term()
				print(f"Searching ({i+1}/{repeats}): {term}")
				perform_search(term, realistic=('realistic' in args))
				if i < repeats - 1:
					wait = random.uniform(5, 15)
					print(f"Waiting {wait:.1f}s before next search...")
					time.sleep(wait)
					resize_and_position_edge()
		else:
			print('Could not launch Microsoft Edge.')

