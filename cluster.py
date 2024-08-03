pip install opencv-python numpy pillow
import cv2
import numpy as np
import time
from PIL import ImageGrab  # For Windows, use PIL.ImageGrab for screenshot capture

# Function to capture a screenshot
def capture_screenshot(bbox=None):
    screen = ImageGrab.grab(bbox=bbox)  # Capture the screen or a specific region
    return np.array(screen)

# Function to analyze the screenshot for issues
def analyze_screenshot(screenshot):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Define a simple threshold for detecting anomalies (e.g., missing information)
    _, thresh_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # Calculate the amount of white (or bright) pixels
    white_pixel_count = np.sum(thresh_image == 255)

    # Define criteria for issue detection (e.g., if white pixel count is below a threshold)
    if white_pixel_count < 1000:  # Adjust the threshold based on your needs
        return True  # Issue detected
    else:
        return False  # No issue

# Function to log issues
def log_issue(issue_detected, timestamp):
    with open("cluster_screen_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - {'Issue Detected' if issue_detected else 'No Issue'}\n")

# Main testing loop
def test_cluster_screen(interval=5, bbox=None):
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        screenshot = capture_screenshot(bbox)
        issue_detected = analyze_screenshot(screenshot)
        
        log_issue(issue_detected, timestamp)

        # Print status to console (optional)
        print(f"{timestamp} - {'Issue Detected' if issue_detected else 'No Issue'}")

        # Wait for the specified interval before capturing the next screenshot
        time.sleep(interval)

# Example usage
# Define the bounding box (left, top, right, bottom) for the screen region
bbox = (100, 100, 800, 600)  # Adjust according to your screen resolution and position

test_cluster_screen(interval=10, bbox=bbox)
