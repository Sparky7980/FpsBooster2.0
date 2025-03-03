import os
import subprocess
import requests
import ctypes
import logging
import platform
import psutil
import time
import sched
import sys

# User's current version
version = 1
login_url = "https://pingreducer2.vercel.app/api/login_storage.json"  # Remote login storage URL

# Directory for logs
program_files_dir = os.path.join(os.environ.get('ProgramFiles', ''), 'PingReducer2')

# Ensure the folder exists
if not os.path.exists(program_files_dir):
    try:
        os.makedirs(program_files_dir)
    except PermissionError:
        print(f"Error creating directory {program_files_dir}. Please run as Administrator.")
        sys.exit(1)

# Log file path
log_file = os.path.join(program_files_dir, 'ping_reducer.log')

# Discord Webhook URL
discord_webhook_reviews_url = "https://discord.com/api/webhooks/1330653431529996348/Kz_umWDfq_KGNSiiNx7WcfuS0TCvlm0SJRbLFe3b0eJQQeTJAYX2xDMKu2j5wjiGfO8o"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# If not running as administrator, request elevation
if not is_admin():
    print("This script requires administrator privileges. Restarting with elevated rights...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
    sys.exit()

# Set up logging to capture errors and debug information in the Program Files folder
logging.basicConfig(filename=log_file, level=logging.DEBUG)

def fetch_latest_version():
    """Fetch the latest version from the API."""
    url = "https://pingreducer2.vercel.app/api/latest_version"  # Replace with the actual URL
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
    user_login = input("Author: Aydin E - Enter login (numeric): ")
    
    if user_login in logins:
        print("Login successful.")
        return True
    else:
        print("Invalid login.")
        logging.warning(f"Failed login attempt: {user_login}")
        return False

def flush_dns():
    """Flush the DNS cache."""
    print("Flushing DNS cache...", end='\r')
    try:
        if os.name == "nt":  # Windows
            subprocess.run("ipconfig /flushdns", check=True, shell=True)
        elif os.name == "posix":  # macOS/Linux
            subprocess.run("sudo dscacheutil -flushcache", check=True, shell=True)
            subprocess.run("sudo killall -HUP mDNSResponder", check=True, shell=True)
        print("DNS cache flushed successfully.", end='\r')
        logging.info("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error flushing DNS: {e}")
        print(f"Error flushing DNS: {e}", end='\r')

def disable_network_throttling():
    """Disable network throttling for gaming."""
    print("Disabling network throttling...", end='\r')
    try:
        if os.name == "nt":  # Windows only
            registry_path = "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile"
            subprocess.run(
                f'reg add "{registry_path}" /v NetworkThrottlingIndex /t REG_DWORD /d 0xffffffff /f',
                check=True, shell=True
            )
            print("Network throttling disabled.", end='\r')
            logging.info("Network throttling disabled.")
        else:
            print("Network throttling adjustments are only supported on Windows.", end='\r')
            logging.warning("Network throttling adjustments are only supported on Windows.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error disabling network throttling: {e}")
        print(f"Error disabling network throttling: {e}", end='\r')

def optimize_tcp_ip():
    """Optimize TCP/IP settings for low latency."""
    print("Optimizing TCP/IP settings...", end='\r')
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
            print("TCP/IP settings optimized.", end='\r')
            logging.info("TCP/IP settings optimized.")
        else:
            print("TCP/IP optimizations are only supported on Windows.", end='\r')
            logging.warning("TCP/IP optimizations are only supported on Windows.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error optimizing TCP/IP settings: {e}")
        print(f"Error optimizing TCP/IP settings: {e}", end='\r')

def run_ping_optimizations():
    """Run all ping optimization steps."""
    flush_dns()
    disable_network_throttling()
    optimize_tcp_ip()
    print("Ping optimizations complete.", end='\r')
    logging.info("Ping optimizations complete.")

def send_feedback_to_discord(feedback):
    """Send the feedback to the Discord webhook."""
    data = {
        "embeds": [
            {
                "title": "Ping Reducer Feedback",
                "color": 16711680,  # Red color (use any color you like)
                "fields": [
                    {
                        "name": "User Feedback",
                        "value": f"Rating: ⭐{feedback} stars",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Feedback received from Ping Reducer Tool"
                }
            }
        ]
    }

    try:
        response = requests.post(discord_webhook_reviews_url, json=data)
        if response.status_code == 204:
            print("Feedback sent to Discord successfully.", end='\r')
        else:
            print(f"Failed to send feedback to Discord: {response.status_code}", end='\r')
    except Exception as e:
        print(f"Error sending feedback to Discord: {e}", end='\r')

def collect_user_feedback():
    """Collect feedback from the user on optimizations."""
    feedback = input("Rate the optimizations (1-5 stars): ")
    if feedback.isdigit() and 1 <= int(feedback) <= 5:
        print("Thank you for your feedback!", end='\r')
        logging.info(f"User rated optimizations: {feedback}")
        send_feedback_to_discord(feedback)  # Send to Discord
    else:
        print("Invalid rating. Please provide a rating between 1 and 5.", end='\r')

def display_system_info():
    """Display basic system information."""
    print("System Information:", end='\r')
    print(f"OS: {platform.system()} {platform.release()} {platform.version()}", end='\r')
    print(f"CPU: {platform.processor()}", end='\r')
    print(f"RAM: {psutil.virtual_memory().total // (1024 ** 2)} MB", end='\r')
    print(f"IP Address: {requests.get('https://api64.ipify.org?format=json').json()['ip']}", end='\r')
    logging.info("System information displayed.")

# Main logic
if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Please run this script as Administrator.", end='\r')
    logging.error("The script was not run as Administrator.")
    exit()

# Login process
if not prompt_login():
    exit()  # Exit if login failed

latest_version = fetch_latest_version()
if latest_version is not None:
    print(f"Latest version: {latest_version}", end='\r')
    
    if version < latest_version:
        print("Your version is outdated.", end='\r')
        print("Please update to the latest version at: https://pingreducer2.vercel.app/", end='\r')
        logging.info("User version is outdated.")
    else:
        print("You are running the latest version!", end='\r')
        logging.info("User is running the latest version.")
else:
    print("Failed to fetch the latest version.", end='\r')
    logging.warning("Failed to fetch the latest version.")

# Await user command to run optimizations
while True:
    user_command = input("Type 'run' to optimize, 'feedback' for feedback, 'info' for system info, 'exit' to quit: ").strip().lower()
    if user_command == "run":
        run_ping_optimizations()
    elif user_command == "feedback":
        collect_user_feedback()
    elif user_command == "info":
        display_system_info()
    elif user_command == "exit":
        print("Exiting the program. Goodbye!", end='\r')
        break
    else:
        print("Invalid command. Please type 'run', 'feedback', 'info', or 'exit'.", end='\r')
