## About the project
This is a project about a Study Assistant that is designed to help users focus during study sessions using preset or custom study techniques. Mainly built in python, it features a timer, a camera to display the countdown and watch the user, and OpenAI's API to give motivational messages and turn those messages into auditory feedback. To let the user know the study session is over or when a milestone has been hit, it'll send a signal to an Arduino to flash an LED light lto communicate to the user and let them know whats happening as to limit distractions from personal devices including their computer. It can also feature a nice visual on the screen while the timer is going as to not distract the user. While the code is running it checks to see if the user is seen on their phone or distracted while in the active study session and it'll alert the user to get back to work. 

## Phases of the project

1. **First working model**
   The first working model includes a camera feature trained with google trainable model to register whether the user it looking at something distracting. It also includes a buzzer to redirect the user when distracted. We utilized python to build the code and environment for this to work alongside an arduino to carry out the messages be the physical model. The main part of this model was training the model and making sure it can run with the arduino setup that we currently have built. The python was constructed to be able to add more and achieve the second model's goals which are more specific to the final model we had in mind. 

2. **Second model** (EDIT BEFORE FINAL)
   We added a timer module to the model for the user to see how much time is left in their study session and to be able to set it to a correct amount of time for the allotted session. It also is able to distinguish among multiple people, people passing by, and other people in the environment, to focus on the main user and not be triggered by others. It included motivating messages by utilizing OpenAI's API and turning those messages into spoken word using a speaker module.

## Install onto your computer

1.  **Clone the repository:**
git clone https://github.com/Im2Slothy/StudyAssistantProject.git
cd StudyAssistantProject



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

## Model Setup (Teachable Machine)

This project uses an image classification model from [Google Teachable Machine](https://teachablemachine.withgoogle.com/).

1. Go to Teachable Machine -> “Image Project”  
2. Train a model (for example: *Focused* vs *Distracted*)  
3. Click **Export Model → TensorFlow → Keras (.h5)**  
4. Download both files:
   - `keras_model.h5`
   - `labels.txt`
5. Create a folder named `personal` in the project and place both files inside:
   ```
   StudyAssistantProject/
   ├─ personal/
   │  ├─ keras_model.h5
   │  ├─ labels.txt
   └─ main.py
   ```

Make sure the filenames and folder name match exactly, since the code loads them from `personal/`. Or just use the files provided with the download off the bat. 


### Accounts & Setup
* **OpenAI API Key:** A valid API key from OpenAI is required and must be stored in the `.env` file. You can get a key from their [API Dashboard](https://platform.openai.com/api-keys)
* **Arduino IDE (Recommended):** Needed to upload the `.ino` sketch to your Arduino board. You could run through VSCode or other methods but it made my life so much easier to just put the code in the Arduino IDE and then just upload it there. 
