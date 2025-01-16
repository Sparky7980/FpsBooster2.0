import os
import subprocess
import requests
import ctypes
import logging
import json
import shutil

# User's current version
version = 1
login_url = "https://fpsbooster2.vercel.app/api/login_storage.json"  # Remote login storage URL
info_url = "https://fpsbooster2.vercel.app/api/info"  # Remote info URL

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
        return response.json()  # Return logins as a dictionary
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching logins: {e}")
        return None

def fetch_system_info():
    """Fetch and display system information from the remote API."""
    try:
        response = requests.get(info_url, timeout=5)
        response.raise_for_status()
        info_data = response.json()
        print("\n--- System Information ---")
        for key, value in info_data.items():
            print(f"{key}: {value}")
        print("\n--- End of Information ---")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching system information: {e}")
    except json.JSONDecodeError:
        print("Error fetching system information: Invalid JSON format.")
        logging.error("Invalid JSON format in system info response.")

def prompt_login():
    """Prompt the user for login and validate against remote data."""
    logins = fetch_logins()
    if logins is None:
        print("Failed to fetch login data. Please try again later.")
        logging.error("Failed to fetch login data.")
        return False
    user_login = input("Enter login (numeric): ")
    if user_login in logins:
        print("Login successful.")
        return True
    else:
        print("Invalid login.")
        logging.warning(f"Failed login attempt: {user_login}")
        return False

def flush_dns():
    """Flush the DNS cache."""
    print("Flushing DNS cache...")
    try:
        if os.name == "nt":  # Windows
            subprocess.run("ipconfig /flushdns", check=True, shell=True)
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error flushing DNS: {e}")

def optimize_power_plan():
    """Switch to high-performance power plan."""
    print("Optimizing power plan for ultimate performance...")
    try:
        if os.name == "nt":  # Windows only
            subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", check=True, shell=True)
            subprocess.run("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61", check=True, shell=True)
        print("Power plan set to Ultimate Performance.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting power plan: {e}")

def terminate_background_processes():
    """Terminate unnecessary background processes."""
    print("Terminating unnecessary background processes...")
    try:
        if os.name == "nt":  # Windows only
            processes_to_kill = ["OneDrive.exe", "Teams.exe"]
            for process in processes_to_kill:
                subprocess.run(f"taskkill /IM {process} /F", check=True, shell=True)
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

def run_ping_optimizations():
    """Run all ping optimization steps."""
    flush_dns()
    optimize_power_plan()
    terminate_background_processes()
    toggle_game_mode(enable=True)

def run_advanced_optimizations():
    """Run advanced optimization features."""
    optimize_power_plan()
    terminate_background_processes()
    toggle_game_mode(enable=True)

def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# Main logic
if not is_admin():
    print("Please run this script as Administrator.")
    exit()

# Login process
if not prompt_login():
    exit()

latest_version = fetch_latest_version()
if latest_version is not None:
    print(f"Latest version: {latest_version}")
    if version < latest_version:
        print("Your version is outdated.")
        print("Please update to the latest version at: https://fpsbooster2.vercel.app")
    else:
        print("You are running the latest version!")
else:
    print("Failed to fetch the latest version.")

# Await user command to run optimizations
while True:
    print("\nCommands:")
    print("1. run - Basic optimizations")
    print("2. advanced - Advanced optimizations")
    print("3. exit - Quit the program")
    print("4. info - nerd")

    user_command = input("Enter your command: ").strip().lower()
    if user_command == "run":
        run_ping_optimizations()
    elif user_command == "advanced":
        run_advanced_optimizations()
    elif user_command == "info":
        fetch_system_info()
    elif user_command == "exit":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid command. Please try again.")
