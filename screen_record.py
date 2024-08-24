import cv2
import numpy as np
import pyautogui
import threading
import time

class ScreenRecorder:
    def __init__(self, filename="screen_recording.mp4", fps=20.0):
        self.filename = filename
        self.fps = fps
        self.recorder = None
        self.recording = False

    def start_recording(self):
        self.recording = True
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.recorder = cv2.VideoWriter(self.filename, fourcc, self.fps, screen_size)

        def record():
            while self.recording:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.recorder.write(frame)

        self.thread = threading.Thread(target=record)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        self.thread.join()
        self.recorder.release()

# In main.py, add:
screen_recorder = ScreenRecorder()

def start_screen_recording():
    screen_recorder.start_recording()

def stop_screen_recording():
    screen_recorder.stop_recording()

# Modify run_app() to use screen recording:
def run_app():
    logging.info("Application started")
    start_screen_recording()
    try:
        # Your app code here
        pass
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())
        capture_screenshot()
    finally:
        stop_screen_recording()