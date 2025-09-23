'''
✅❌⌛(Done, Not Done, In Progress)

✅ Welcome the user
 
❌ find someway for the user to give the topic or photos/pdfs of what they're working with if they choose. 

✅ Ask the user for a specific study method or a simple timer. 
✅ Maybe a config for different study methods? ( This does this and that - Have them enter their choice via numbers or text ) - use.lower (DONE with IDs)

❌ When we're ready to begin, ensure we have camera access - Document in comments or somewhere to help the user solve the errors.

❌ When we're started, say X photos a second or every few seconds -- We'll compare what we see with the trained model --
❌If user is caught using phone
  Work with arduino to play buzzer -- Are we doing something with the time?
else:
  Continue and play a task or loop to take photos and check.

  
✅While this is happening we either play the timer on the screen or just print every minute in the console. 

❌When we hit milestones (Specify in the config -- Tell the user they're doing)

❌Integrate ChatGPT into the code for checks of assignment and stuff - run this last. 

Future ideas:
- maybe add microphone input for study method instead of typing/ID
- tie Arduino + camera into same loop as timer ( We are going to use the device camera per prof.)
- milestone notifications every X cycles ( Yay congrats, keep going!, etc etc)
'''




import time
import cv2   # camera
import serial  # arduino
from config import study_methods

# ---------------- ARDUINO SETUP ----------------
# Adjust the port 
try:
    arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)
    print("Arduino connected.")
except Exception as e:
    print("Arduino not connected:", e)
    arduino = None


# ---------------- CAMERA FUNCTIONS ----------------
def start_camera(desired_fps=30):
    """Start camera capture3"""
    cap = cv2.VideoCapture(0)  # default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    cap.set(cv2.CAP_PROP_FPS, desired_fps)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Camera started. Requested FPS: {desired_fps}, Actual FPS: {actual_fps}")
    return cap

def stop_camera(cap):
    if cap:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera stopped.")


# ---------------- TIMER FUNCTIONS ----------------
def run_timer(work_time, break_time, cycles):
    #print("run timer started")
    print("work_time:", work_time, "break_time:", break_time, "cycles:", cycles)

    cap = start_camera()

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

    stop_camera(cap)


def countdown(seconds, cap=None):
    #print("countdown started with seconds ", seconds)

    end_time = time.time() + seconds  # mark when countdown should end

    while time.time() < end_time:
        # calculate remaining time
        remaining = int(end_time - time.time())
        mins, secs = divmod(remaining, 60)
        print(f"{mins:02d}:{secs:02d} remaining", end="\r")

        # update camera frame if available
        if cap:
            ret, frame = cap.read()
            if ret:
                # overlay countdown timer on video feed
                cv2.putText(frame, f"{mins:02d}:{secs:02d}",
                            (30, 50),               # position
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)

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
                print("Value must be at least 1. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


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
        #print("i choose ", choice)

        for name, details in study_methods.items():
            if choice == str(details["id"]) or choice == name:
                selected_method = name
                break

        if not selected_method:
            print("Invalid choice. Try again.")

    config = study_methods[selected_method]
    print(config)

    # if they choose custom ask what they want
    if selected_method == "custom":
        print("Custom  selected")

        work_time = get_positive_int("Enter study time (minutes): ") * 60
        break_time = get_positive_int("Enter break time (minutes): ") * 60
        cycles = get_positive_int("Enter number of cycles: ")

        print("Custom values ->", work_time, break_time, cycles)
    else:
        work_time = config["work_time"]
        break_time = config["break_time"]
        cycles = config["cycles"]

    #print("Starting timer with:", work_time, break_time, cycles) 
    run_timer(work_time, break_time, cycles)


if __name__ == "__main__":
    print("start")
    main()
