## About the project
This is a Study Assistant designed to help users maintain focus during study sessions using preset or custom study techniques. Built primarily in Python, it features: 
- A session timer
-  A camera for countdown display and focus monitoring
-  Integration with OpenAI's API to generate motivational prompts and convert them into audio feedback.
-  Arduino-based LED signaling for milestones, reducing reliance on distracting personal devices
-  Distraction detection, alerting the user when they appear to be using their phone or looking away.

## Phases of the project

1. **First working model**
   
   The first working model included:
   - A camera feature trained using a Google Teachable Model to classify user focus
   - An Arduino-connected buzzer to redirect distracted users
   - A Python environment designed to support future modular expansion

2. **Second model**
   
    In this phase, we focused on implementing text-to-speech features. We experienced challenges with:
   - Model communication delays
   - Inconsistent audio playback
   Despite this, we achieved more accurate buzzer signaling

   Our goals for the next demo include: 
   - Getting text-to-speech functioning reliably
   - Beginning to work on the session timer
   - Question and Answer session to quiz the user using a PDF reader

3. **Third model(Final model)**
   
 In this final phase, we:
   - Optimized the code to make camera-model interactions smoother
   - Attempted to resolve issues with the model misidentifying certain group members
   - Implemented a GPT-based question generator to quiz users after their study session
   - Added a PDF-import option, prompting the user at startup to upload a file used for generating questions later

## Overall ## 
We are very proudo of the progress made throughout this project. We successfully achieved most of our planned features and created a functioning integrated system. 

With additional time we would: 
- Optimize model accuracy and camera interaction
- Train on a more diverse dataset to reduce misclassification
- Improve user recognition vs nearby bystanders

Overall, the system performed reliably and the results were rewarding!

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
