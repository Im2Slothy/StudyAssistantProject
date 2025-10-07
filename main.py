import time
import cv2   # camera
import serial  # arduino
from config import study_methods
import os
import threading
import queue
import pygame  # this is playing the audio 
from vosk import Model as VoskModel, KaldiRecognizer
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


# ---------------- ARDUINO SETUP ----------------
# Adjust the port, if you need help finding this go to device manager on Windows or use `ls /dev/tty.*` on Mac/Linux
try:
    arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)
    print("Arduino connected.")
except Exception as e:
    print("Arduino not connected:", e)
    arduino = None


# ---------------- CAMERA FUNCTIONS ----------------
class CustomDepthwiseConv2D(DepthwiseConv2D):  # This function detects what the camera is looking at
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)
        super().__init__(*args, **kwargs)


# Load phone detection model once at startup
try:
    import numpy as np
    np.set_printoptions(suppress=True)
    # Try loading the model without custom objects first
    phone_model = load_model("Image_Models/keras_model.h5", compile=False)
    class_names = open("Image_Models/labels.txt", "r").readlines()
    print("Phone detection model loaded successfully!")
    MODEL_LOADED = True

except Exception as e:
    print(f"Could not load phone detection model: {e}")
    print("Continuing without phone detection...")
    phone_model = None
    class_names = None
    MODEL_LOADED = False


def detect_phone_in_frame(frame):
    """Detect if phone is in the camera frame"""
    if not MODEL_LOADED or phone_model is None:
        return False

    try:
        # Resize frame to model input size
        resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

        # Prepare for model prediction
        image_array = np.asarray(resized, dtype=np.float32).reshape(1, 224, 224, 3)
        normalized_image = (image_array / 127.5) - 1

        # Make prediction
        prediction = phone_model.predict(normalized_image, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index].strip()
        confidence = prediction[0][index]

        # Check if phone is detected with high confidence
        if "phone" in class_name.lower() and confidence > 0.7:
            print(f"Phone detected! Confidence: {confidence:.2f}")
            return True

        return False

    except Exception as e:
        print(f"Error in phone detection: {e}")
        return False


def start_camera(desired_fps=30):
    """Start camera capture"""
    cap = cv2.VideoCapture(0)  # default camera

    if not cap.isOpened():
        print("Error: Could not open camera. If you're getting this error, try checking your camera permissions or if another application is using the camera.")
        return None

    cap.set(cv2.CAP_PROP_FPS, desired_fps)
    return cap


def stop_camera(cap):
    if cap:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera stopped.")


# ---------------- TIMER FUNCTIONS ----------------
def run_timer(work_time, break_time, cycles):
    print("work_time:", work_time, "break_time:", break_time, "cycles:", cycles)

    cap = start_camera()
    if cap is None:
        print("Camera not available. Running without camera detection.")

    # start motivational worker thread
    stop_nice = threading.Event()
    motivation_interval = 300  # 5 minutes between motivational phrases
    nice_thread = threading.Thread(target=nice_worker, args=(stop_nice, motivation_interval), daemon=True)
    nice_thread.start()

    try:
        for cycle in range(1, cycles + 1):
            print("\nCycle:", cycle)

            # Work phase
            print("\nStarting study phase")
            countdown(work_time, cap)

            # Break phase
            print("\nStarting break phase")
            countdown(break_time, cap)

            print("Cycle complete:", cycle)

        print("All cycles complete")

        # send signal to Arduino when finished
        if arduino:
            arduino.write(b"light\n")

    finally:
        # stop motivational thread
        stop_nice.set()
        nice_thread.join(timeout=2)  # wait 2 seconds for thread to stop
        stop_camera(cap)


def countdown(seconds, cap=None):
    # Timer countdown function
    end_time = time.time() + seconds

    while time.time() < end_time:
        remaining = int(end_time - time.time())
        mins, secs = divmod(remaining, 60)
        print(f"{mins:02d}:{secs:02d} remaining", end="\r")

        # update camera frame if available
        if cap:
            ret, frame = cap.read()
            if ret:
                # Check for phone if model is loaded
                phone_detected = False
                if MODEL_LOADED and phone_model is not None:
                    phone_detected = detect_phone_in_frame(frame)

                    if phone_detected:
                        # Flash red warning if phone detected
                        cv2.putText(frame, "PHONE DETECTED!", (30, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        # Send warning to Arduino
                        if arduino:
                            arduino.write(b"phone_warning\n")

                # overlay countdown timer on video feed
                timer_color = (0, 0, 255) if phone_detected else (0, 255, 0)  # Red if phone, green otherwise
                cv2.putText(frame, f"{mins:02d}:{secs:02d}",
                            (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, timer_color, 2, cv2.LINE_AA)

                cv2.imshow("Study Helper Camera", frame)

                # allow quitting camera early
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        # stackoverflow says sleep to prevent the CPU from being overworked
        time.sleep(0.03)

    print("countdown finished")


# ---------------- INPUT VALIDATION ----------------
def get_positive_int(prompt):
    """Keep asking until user gives a valid integer >= 1"""
    while True:
        try:
            value = int(input(prompt))
            if value < 1:
                print("Please enter a number greater than 0")
                continue
            return value
        except:
            print("That's not a valid number, try again")


# ---------------- MAIN MENU ----------------
def main():
    print("Welcome to our study helper")
    print("Choose a study method below:")

    # Show available methods with IDs
    for name, details in study_methods.items():
        print(details["id"], "-", name, ":", details["description"])

    selected_method = None

    # Keep asking until valid input
    while not selected_method:
        choice = input("Enter method ID or name: ").strip().lower()

        for name, details in study_methods.items():
            if choice == str(details["id"]) or choice == name:
                selected_method = name
                break

        if not selected_method:
            print("That's not a valid option, try again")

    config = study_methods[selected_method]
    print(config)

    # if they choose custom ask what they want
    if selected_method == "custom":
        work_time = get_positive_int("How many minutes to study? ") * 60
        break_time = get_positive_int("How many minutes for breaks? ") * 60
        cycles = get_positive_int("How many cycles? ")
    else:
        # Use the preset values
        work_time = config["work_time"]
        break_time = config["break_time"]
        cycles = config["cycles"]

    run_timer(work_time, break_time, cycles)


# ---------------- TTS SETUP ----------------
tts_queue = queue.Queue()
tts_stop_event = threading.Event()


def tts_worker():
    # This function runs in the background to handle TTS
    client = OpenAI()

    while not tts_stop_event.is_set():
        try:
            phrase = tts_queue.get(timeout=0.5)

            try:
                # Generate and play audio
                response = client.audio.speech.create(model="tts-1", voice="alloy", input=phrase) # This model is cheap and sounds good so we should use it.


                # Write to temp file and play immediately
                with open("temp_tts.mp3", "wb") as f:
                    f.write(response.content)

                # Play audio using pygame - I've used idk how many more methods with the help of AI and this is the only one that works.
                pygame.mixer.init()
                pygame.mixer.music.load("temp_tts.mp3")
                pygame.mixer.music.play()

                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                pygame.mixer.quit()
                print("TTS done!")

            except Exception as e:
                print(f"TTS Error: {e}")

        except queue.Empty:
            continue


def speak_text(text):
    """Add text to TTS queue"""
    tts_queue.put(text)


# Start TTS worker once at program start
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()


# ---------------- PHRASE WORKER ----------------
def nice_worker(stop_event, interval_seconds=300):
    """Fetch phrases every interval and queue them for TTS"""
    client = OpenAI()

    def get_nice_phrase_from_api():
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly, creative study coach. Each message should feel different. "
                            "Avoid repeating words or phrasing. No Emojis. Keep it under 25 words."
                        ),
                    },
                    {"role": "user", "content": "Give one short, unique, encouraging sentence for someone studying."}
                ],
                max_tokens=40,
                temperature=0.9,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting motivation: {e}")
            return None

    # send first phrase immediately
    phrase = get_nice_phrase_from_api()
    if phrase:
        speak_text(phrase)

    # then loop every interval
    last_time = time.time()

    # loop until stopped
    while not stop_event.is_set():
        current_time = time.time()
        time_since_last = current_time - last_time

        # if enough time has passed, get a new phrase
        if time_since_last >= interval_seconds:
            phrase = get_nice_phrase_from_api()
            if phrase:
                print(f"Motivation: {phrase}")
                speak_text(phrase)
                last_time = current_time

        time.sleep(0.5)


# ---------------- RUN MAIN ----------------
if __name__ == "__main__":
    print("start")

    try:
        main()
    finally:
        # Cleanup on exit
        tts_stop_event.set()
        tts_thread.join(timeout=2)

        # Remove temp file if it exists
        if os.path.exists("temp_tts.mp3"):
            os.remove("temp_tts.mp3")

        print("Cleanup complete")
