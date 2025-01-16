import os
import subprocess
import requests
import ctypes
import logging
import json

# User's current version
version = 1
login_url = "https://fpsbooster2.vercel.app/api/login_storage.json"  # Remote login storage URL

# Set up logging to capture errors and debug information
logging.basicConfig(filename='fps_booster.log', level=logging.DEBUG)

def fetch_latest_version():
    """Fetch the latest version from the API."""
    url = "https://fpsbooster2.vercel.app/api/latest_version"  # Replace with the actual URL
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

def prompt_login():
    """Prompt the user for login and validate against remote data."""
    logins = fetch_logins()
    
    if logins is None:
        print("Failed to fetch login data. Please try again later.")
        logging.error("Failed to fetch login data.")
        return False
    
    # Prompt the user for login
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
        elif os.name == "posix":  # macOS/Linux
            subprocess.run("sudo dscacheutil -flushcache", check=True, shell=True)
            subprocess.run("sudo killall -HUP mDNSResponder", check=True, shell=True)
        print("DNS cache flushed successfully.")
        logging.info("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error flushing DNS: {e}")
        print(f"Error flushing DNS: {e}")

def disable_network_throttling():
    """Disable network throttling for gaming."""
    print("Disabling network throttling...")
    try:
        if os.name == "nt":  # Windows only
            registry_path = "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile"
            subprocess.run(
                f'reg add "{registry_path}" /v NetworkThrottlingIndex /t REG_DWORD /d 0xffffffff /f',
                check=True, shell=True
            )
            print("Network throttling disabled.")
            logging.info("Network throttling disabled.")
        else:
            print("Network throttling adjustments are only supported on Windows.")
            logging.warning("Network throttling adjustments are only supported on Windows.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error disabling network throttling: {e}")
        print(f"Error disabling network throttling: {e}")

def optimize_tcp_ip():
    """Optimize TCP/IP settings for low latency."""
    print("Optimizing TCP/IP settings...")
    try:
        if os.name == "nt":  # Windows only
            registry_path = "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters"
            subprocess.run(
                f'reg add "{registry_path}" /v TcpAckFrequency /t REG_DWORD /d 1 /f',
                check=True, shell=True
            )
            subprocess.run(
                f'reg add "{registry_path}" /v TCPNoDelay /t REG_DWORD /d 1 /f',
                check=True, shell=True
            )
            print("TCP/IP settings optimized.")
            logging.info("TCP/IP settings optimized.")
        else:
            print("TCP/IP optimizations are only supported on Windows.")
            logging.warning("TCP/IP optimizations are only supported on Windows.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error optimizing TCP/IP settings: {e}")
        print(f"Error optimizing TCP/IP settings: {e}")

def apply_ultimate_performance_plan():
    """Enable Ultimate Performance power plan on Windows."""
    print("Enabling Ultimate Performance power plan...")
    try:
        # Add the Ultimate Performance plan
        subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", check=True, shell=True)
        # Try to set Ultimate Performance as the active plan
        subprocess.run("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61", check=True, shell=True)
        print("Ultimate Performance power plan applied.")
        logging.info("Ultimate Performance power plan applied.")
    except subprocess.CalledProcessError:
        print("Ultimate Performance plan not available, falling back to High-Performance plan.")
        logging.warning("Ultimate Performance plan not available, falling back to High-Performance plan.")
        # Fall back to High-Performance plan (usually GUID: 8c5e7fda-60b1-4c8b-ae4f-485b6e5fdaea)
        subprocess.run("powercfg -setactive 8c5e7fda-60b1-4c8b-ae4f-485b6e5fdaea", check=True, shell=True)
        print("High-Performance power plan applied.")
        logging.info("High-Performance power plan applied.")


def run_ping_optimizations():
    """Run all ping optimization steps."""
    flush_dns()
    disable_network_throttling()
    optimize_tcp_ip()
    apply_ultimate_performance_plan()  # Apply Ultimate Performance plan
    print("Ping optimizations complete.")
    logging.info("Ping optimizations complete.")

# Main logic
if not is_admin():
    print("Please run this script as Administrator.")
    logging.error("The script was not run as Administrator.")
    exit()

# Login process
if not prompt_login():
    exit()  # Exit if login failed

latest_version = fetch_latest_version()
if latest_version is not None:
    print(f"Latest version: {latest_version}")
    
    if version < latest_version:
        print("Your version is outdated.")
        print("Please update to the latest version at: https://fpsbooster2.vercel.app")
        logging.info("User version is outdated.")
    else:
        print("You are running the latest version!")
        logging.info("User is running the latest version.")
else:
    print("Failed to fetch the latest version.")
    logging.warning("Failed to fetch the latest version.")

# Await user command to run optimizations
while True:
    user_command = input("Type 'run' to optimize or 'exit' to quit: ").strip().lower()
    if user_command == "run":
        run_ping_optimizations()
    elif user_command == "exit":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid command. Please type 'run' or 'exit'.")
