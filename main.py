import time
import os
import cv2
import numpy as np
import pyautogui
from pynput import keyboard

# Folder for storing data
output_folder = "dataset"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# File for key press logs
log_file = os.path.join(output_folder, 'key_log.txt')

# Flag variable for stopping the recording
recording = True

# Log key presses
def log_key(key):
    global recording
    timestamp = time.time()

    try:
        key_pressed = key.char  # Character (e.g., 'w', 'a', 's', 'd')
    except AttributeError:
        key_pressed = str(key)  # Special keys (e.g., 'Key.space', 'Key.f12')

    with open(log_file, 'a') as f:
        f.write(f'{timestamp},{key_pressed}\n')

    # If F12 is pressed — exit
    if key == keyboard.Key.f12:
        print("[INFO] Recording stopped by user.")
        recording = False
        return False  # Stop the listener

# Function to capture screenshots
def capture_screen():
    timestamp = time.time()
    screenshot = pyautogui.screenshot()  # Take a screenshot
    frame = np.array(screenshot)  # Convert to numpy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to OpenCV format
    filename = os.path.join(output_folder, f"{timestamp}.jpg")
    cv2.imwrite(filename, frame)  # Save the screenshot

# Main function
def start_recording():
    global recording
    with keyboard.Listener(on_press=log_key) as listener:
        while recording:
            capture_screen()  # Record a frame
            time.sleep(0.2)  # 5 frames per second
        listener.stop()

if __name__ == '__main__':
    print("[INFO] Recording started. Press F12 to stop.")
    start_recording()