## About the project
This is a project about a Study Assistant that is designed to help users focus during study sessions using preset or custom study techniques. Mainly built in python you it features a timer, a camera to display the countdown and watch the user, and OpenAI's API to give motivational messages and turn said messages into spoken voice. To let the user know the study session is over or when a milestone has been hit it'll send a signal to an Arduino to flash an LED light letting the user know whats happening so they can have the computer in the background and just have the nice visual in front of them. While the code is running it'll be checking to see if the user is seen on their phone distracted while in the active study session and it'll alert the user to get back to work. 

## Install onto your computer

1.  **Clone the repository:**
    ```bash
    git [clone https://github.com/Im2Slothy/StudyAssistantProject](https://github.com/Im2Slothy/StudyAssistantProject.git)
    cd StudyAssistantProject
    ```

2.  **Set up the Environment:**
    Create a file named `.env` in the main project folder and add your OpenAI API key to it:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```

3.  **Install Dependencies:**
    Install all the required Python libraries by running the following command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Connect Hardware:**
    Upload the `main.ino` sketch to your Arduino and connect it to your computer. You may need to update the COM port in the `main.py` file if it's not on `COM3`.

## Requirements 

### Hardware
* A computer with Python installed.
* A webcam.
* An Arduino board (e.g., Arduino Uno).
* An LED with appropriate wires and resistors.

### Accounts & Setup
* **OpenAI API Key:** A valid API key from OpenAI is required and must be stored in the `.env` file. You can get a key from their [API Dashboard](https://platform.openai.com/api-keys)
* **Arduino IDE (Recommended):** Needed to upload the `.ino` sketch to your Arduino board. You could run through VSCode or other methods but it made my life so much easier to just put the code in the Arduino IDE and then just upload it there. 
