## About the project
This is a project about a Study Assistant that is designed to help users focus during study sessions using preset or custom study techniques. Mainly built in python, it features a timer, a camera to display the countdown and watch the user, and OpenAI's API to give motivational messages and turn those messages into auditory feedback. To let the user know the study session is over or when a milestone has been hit, it'll send a signal to an Arduino to flash an LED light lto communicate to the user and let them know whats happening as to limit distractions from personal devices including their computer. It can also feature a nice visual on the screen while the timer is going as to not distract the user. While the code is running it checks to see if the user is seen on their phone or distracted while in the active study session and it'll alert the user to get back to work. 

## Phases of the project

1. **First working model**
   The first working model includes a camera feature trained with google trainable model to register whether the user it looking at something distracting. It also includes a buzzer to redirect the user when distracted. We utilized python to build the code and environment for this to work alongside an arduino to carry out the messages be the physical model. The main part of this model was training the model and making sure it can run with the arduino setup that we currently have built. The python was constructed to be able to add more and achieve the second model's goals which are more specific to the final model we had in mind. 

2. **Second model** 
    This model, we tried to figure out the text to speech section of the model. But we had some trouble getting it to communicate with the model, so we got the buzzer working pretty accurately. We tried multiple things to try and get the text to speech to work but there were a lot of delays and flaws within what it was recognizing and when it would play the sound. Our main goal for the next demo is to get the text to speech working the way we want it to and maybe dedicating some time to trying to implement the timer, but it depends on how much time and trouble the text to speech gives us.

3. **Third model**

## Requirements

### Hardware
* A computer with Python installed.
* A webcam.
* An Arduino board (e.g., Arduino Uno).

### Software & Accounts
* **Python 3.11+:** This project was built and tested on **Python 3.11.8**. It's not guaranteed to work on other versions.
* **Required Libraries:** All Python packages are listed in `requirements.txt`.
* **OpenAI API Key:** A valid API key from OpenAI is required for the motivational coach and the PDF Q&A. You can get a key from their [API Dashboard](https://platform.openai.com/api-keys).
* **Arduino IDE (Recommended):** Needed to upload the `.ino` sketch to your Arduino board. It's just the easiest way to do it.

---

## Install onto your computer

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Im2Slothy/StudyAssistantProject.git](https://github.com/Im2Slothy/StudyAssistantProject.git)
    cd StudyAssistantProject
    ```

2.  **Set up the Environment:**
    Create a file named `.env` in the main project folder and add your OpenAI API key to it:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```

3.  **Install Dependencies:**
    Install all the required Python libraries using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    > **Heads up!** As mentioned, this was tested on **Python 3.11.8**. If you run into issues, the package versions in the `requirements.txt` file are the ones that are known to work.

4.  **Connect Hardware:**
    Upload the `main.ino` sketch to your Arduino and connect it to your computer.
    
    **Important:** You may need to update the COM port in `main.py` if it's not on `COM3`. You can find the correct port in the Arduino IDE or your computer's Device Manager.
    ```python
    # main.py
    arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1) 
    ```

---

## How to Use

1.  **Run the script:**
    ```bash
    python main.py
    ```

2.  **(Optional) Upload PDF:** The script will first ask if you want to upload a PDF for a Q&A session. If you type `y`, it will ask you to drag and drop the file into the console and press Enter.

3.  **Choose Method:** Select your preferred study method (like "pomodoro" or "custom") from the menu.

4.  **Get to Work!** The timer will start, and your webcam feed will appear. The model will now watch for distractions. If it detects you're looking away, it'll trigger the Arduino buzzer and tell you to get back on task.

5.  **Review (If PDF was loaded):** After all your study/break cycles are finished, the script will connect to GPT, analyze your PDF text, and print a custom set of questions and answers to help you review.

---

## Model Setup (Teachable Machine)

This project uses an image classification model from [Google Teachable Machine](https://teachablemachine.withgoogle.com/). You can use the model I've already trained (in the `mikeModels` folder) or train your own.

**To train your own:**

1.  Go to Teachable Machine -> “Image Project”
2.  Train a model (for example: **Class 0: Focused** vs **Class 1: Distracted**).
    *Note: The code is hard-wired to treat `index == 1` as the "distracted" class.*
3.  Click **Export Model → TensorFlow → Keras (.h5)**
4.  Download both files:
    * `keras_model.h5`
    * `labels.txt`
5.  Create a folder named `mikeModels` (or change the path in `main.py`) and place both files inside:
    ```
    StudyAssistantProject/
    ├─ mikeModels/
    │  ├─ keras_model.h5
    │  └─ labels.txt
    └─ main.py
    ```

## Configuration

The `main.py` file has a "CONFIG VARIABLES" section at the top. You can easily change settings there without digging into the code:

* `preset_dir`: The folder where your *distraction alert* MP3s are stored (default is `"GPTPresetMP3"`). You'll need to create this folder and add your own MP3s.
* `alert_delay_after_buzzer`: How long to wait (in seconds) after the buzzer before playing the voice alert.
* `alert_cooldown`: How long to wait between distraction alerts, so you don't get spammed.
* `start_delay`: A grace period (in seconds) at the beginning of a session before the distraction alerts are active.

## Issues
If you encounter issues, you can throw them in the GitHub issues area. This was a semester project, so I more than likely WONT be looking at this again, but you never know!
