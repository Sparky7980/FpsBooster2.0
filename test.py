import os
import subprocess
import requests
import ctypes
import logging
import shutil

# User's current version
version = 1
login_url = "https://fpsbooster2.vercel.app/api/login_storage.json"  # Remote login storage URL

# Set up logging to capture errors and debug information
logging.basicConfig(filename='fps_booster.log', level=logging.DEBUG)

def fetch_latest_version():
    """Fetch the latest version from the API."""
    url = "https://fpsbooster2.vercel.app/api/latest_version"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return float(response.text.strip())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching latest version: {e}")
        return None
    except ValueError:
        logging.error("Error: The response is not a valid version number.")
        return None

def fetch_logins():
    """Fetch the login data from the remote server."""
    try:
        response = requests.get(login_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching logins: {e}")
        return None

def prompt_login():
    """Prompt the user for login and validate against remote data."""
    logins = fetch_logins()
    
    if logins is None:
        print("Failed to fetch login data. Please try again later.")
        logging.error("Failed to fetch login data.")
        return False
    
    user_login = input("Enter login (numeric): ").strip()
    
    if user_login in logins:
        print("Login successful.")
        return True
    else:
        print("Invalid login.")
        logging.warning(f"Failed login attempt: {user_login}")
        return False

def fetch_info():
    """Fetch system information from the API and display it."""
    url = "https://fpsbooster2.vercel.app/api/info"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        info_data = response.json()
        print("\nSystem Information:")
        for key, value in info_data.items():
            print(f"{key}: {value}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching system information: {e}")
        logging.error(f"Error fetching system information: {e}")

def flush_dns():
    """Flush the DNS cache."""
    print("Flushing DNS cache...")
    try:
        if os.name == "nt":
            subprocess.run("ipconfig /flushdns", check=True, shell=True)
        elif os.name == "posix":
            subprocess.run("sudo dscacheutil -flushcache", check=True, shell=True)
            subprocess.run("sudo killall -HUP mDNSResponder", check=True, shell=True)
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error flushing DNS: {e}")

def system_cleanup():
    """Clean up temporary files and system cache."""
    print("Cleaning up system temporary files...")
    try:
        if os.name == "nt":
            temp_path = os.environ.get("TEMP", "")
            shutil.rmtree(temp_path, ignore_errors=True)
            subprocess.run("cleanmgr /sagerun:1", check=True, shell=True)
        else:
            print("System cleanup is only supported on Windows.")
        print("System cleanup completed.")
    except Exception as e:
        print(f"Error during system cleanup: {e}")

def optimize_power_plan():
    """Switch to high-performance power plan."""
    print("Optimizing power plan for ultimate performance...")
    try:
        if os.name == "nt":
            subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", check=True, shell=True)
        else:
            print("Power plan optimization is only supported on Windows.")
        print("Power plan set to Ultimate PC.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting power plan: {e}")

def terminate_background_processes():
    """Terminate unnecessary background processes."""
    print("Terminating unnecessary background processes...")
    try:
        if os.name == "nt":
            processes_to_kill = ["OneDrive.exe", "Teams.exe"]
            for process in processes_to_kill:
                subprocess.run(f"taskkill /IM {process} /F", check=True, shell=True)
        else:
            print("Background process termination is only supported on Windows.")
        print("Background processes terminated.")
    except subprocess.CalledProcessError as e:
        print(f"Error terminating processes: {e}")

def toggle_game_mode(enable=True):
    """Enable or disable Windows Game Mode."""
    print(f"{'Enabling' if enable else 'Disabling'} Game Mode...")
    try:
        registry_path = "HKCU\\Software\\Microsoft\\GameBar"
        value = 1 if enable else 0
        subprocess.run(
            f'reg add "{registry_path}" /v AllowAutoGameMode /t REG_DWORD /d {value} /f',
            check=True, shell=True
        )
        print(f"Game Mode {'enabled' if enable else 'disabled'}.")
    except subprocess.CalledProcessError as e:
        print(f"Error toggling Game Mode: {e}")

def run_advanced_optimizations():
    """Run advanced optimization features."""
    system_cleanup()
    optimize_power_plan()
    terminate_background_processes()
    toggle_game_mode(enable=True)

def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

if not is_admin():
    print("Please run this script as Administrator.")
    exit()

if not prompt_login():
    exit()

latest_version = fetch_latest_version()
if latest_version is not None:
    print(f"Latest version: {latest_version}")
    if version < latest_version:
        print("Your version is outdated. Update at https://fpsbooster2.vercel.app.")
    else:
        print("You are running the latest version!")
else:
    print("Failed to fetch the latest version.")

# Command loop
while True:
    print("\nCommands:")
    print("1. run - Basic optimizations")
    print("2. advanced - Advanced optimizations")
    print("3. exit - Quit the program")
    print("4. info - Fetch system information")
    
    user_command = input("Enter your command: ").strip().lower()
    
    if user_command in ("run", "1"):
        flush_dns()
    elif user_command in ("advanced", "2"):
        run_advanced_optimizations()
    elif user_command in ("info", "4"):
        fetch_info()
    elif user_command in ("exit", "3"):
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid command. Please try again.")
