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

def fetch_info():
    """Fetch the information from the API and print it."""
    try:
        response = requests.get(info_url, timeout=5)
        response.raise_for_status()
        info_data = response.json()  # Expecting JSON response
        print("\n=== System Information ===")
        for key, value in info_data.items():
            print(f"{key}: {value}")
        print("=========================\n")
        logging.info("Info fetched and displayed successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching info: {e}")
        print("Failed to fetch information. Please try again later.")
    except ValueError:
        logging.error("Error: The response is not valid JSON.")
        print("Failed to fetch information. Please try again later.")

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

# Add other functions like flush_dns(), system_cleanup(), etc. from your previous script.

# Main logic
if not ctypes.windll.shell32.IsUserAnAdmin():
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
    print("\nCommands:")
    print("1. run - Basic optimizations")
    print("2. advanced - Advanced optimizations")
    print("3. exit - Quit the program")
    print("4. info - Nerd stuff 🤓")
    
    user_command = input("Enter your command: ").strip().lower()
    if user_command == "run":
        print("Running basic optimizations...")
        # Add the function call for basic optimizations
    elif user_command == "advanced":
        print("Running advanced optimizations...")
        # Add the function call for advanced optimizations
    elif user_command == "info":
        print("Fetching system information...")
        fetch_info()
    elif user_command == "exit":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid command. Please try again.")
