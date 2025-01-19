import cv2
import time
import requests

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1330674445865586728/W2BI-bA25yoVHs0XTclaneW7mXtp-Dhhw_eB8sHQDtw8fCzvVm88riYSkJ14etboAaBE"

def stream_video_to_webhook(webhook_url, video_source=0, frame_interval=1):
    """
    Streams video to a Discord webhook by sending frames as image files.

    :param webhook_url: The Discord webhook URL
    :param video_source: Video source for OpenCV (default is 0 for webcam)
    :param frame_interval: Time in seconds between sending each frame
    """
    # Open a connection to the video source
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Unable to access the video source.")
        return

    try:
        print("Streaming video. Press Ctrl+C to stop.")
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

            # Send the frame to the webhook
            response = requests.post(webhook_url, files=files)
            if response.status_code != 204:
                print(f"Error: Failed to send frame. Status code: {response.status_code}, Response: {response.text}")
            
            # Wait before sending the next frame to simulate a stream
            time.sleep(frame_interval)
    except KeyboardInterrupt:
        print("\nStreaming stopped.")
    finally:
        # Release the video capture
        cap.release()

# Run the video streaming function
if __name__ == "__main__":
    stream_video_to_webhook(WEBHOOK_URL, video_source=0, frame_interval=1)
