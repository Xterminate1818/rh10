# Reinforcement Learning

This repo followed the 4-part tutorial series by [Sentdex](https://www.youtube.com/@sentdex) on YouTube, [Reinforcement Learning with Stable Baselines 3](https://www.youtube.com/playlist?list=PLQVvvaa0QuDf0O2DWwLZBfJeYY-JOeZB1). The Sentdex tutorials are what provided me with the know-how for developing a *Snake Game* environment. 

After completing the Sentex tutorials I continued to develop the code-base with rewrites, refactors, and upgrades to make things easier in the long term. 

The code-base now serves as a means of training and evaluating a RL agent against a Snake Game environment. 

## Getting Started

To get started with this repo, here's a list of next steps.

- [x] [Clone this repo to your machine](#clone-this-repo-to-your-machine)
- [x] [Open this repo in VS Code as a workspace](#open-this-repo-in-VS-Code-as-a-workspace)
- [x] [Download and install Python](#download-and-install-Python)
- [x] [Create a VENV for this project](#create-a-venv-for-this-project)
- [x] [Activate the VENV you just created in a VS Code cmd terminal](#activate-the-venv-you-just-created-in-a-vs-code-cmd-terminal)
- [x] [Download and install PyTorch](#download-and-install-pytorch)
- [x] [Download and install Gymnasium](#download-and-install-gymnasium)
- [x] [Download and install Stable Baselines 3](#download-and-install-stable-baselines-3)
- [x] [Download and install TensorFlow](#download-and-install-tensorflow)
- [x] [Running the code](#running-the-code)
- [x] [View logs by running TensorBoard](#view-logs-by-running-tensorboard)
- [x] [Generate a dependencies file to save package versions](#generate-a-dependencies-file-to-save-package-versions)
 
## Clone this repo to your machine

### ...manually

- In the top-right corner of this page, you should see a blue button with a drop down arrow that is labeled "Code". Click it to open the drop-down menu
- In the drop-down menu, in the section labeled "Download soure code", select "zip"
- Place the .zip file wherever you prefer on your machine
- Unpack the .zip file

### ...using CMD/Command Line (Windows)

- Open a CMD terminal by pressing the windows key, typing "cmd" and pressing enter
- Confirm you have [git](https://git-scm.com/download/win) by typing ```git --version``` and pressing enter
    - You should see the terminal reply something like, "git version a.b.c"
- Add your GitLab name by typing into the terminal ```git config --global user.name "Your Name"```
- Add your GitLab email by typing into the terminal ```git config --global user.email "your_email@domain.com"```
- Confirm you did it by typing ```git config --global --list```
- In the top-right corner of this page, you should see a blue button with a drop down arrow that is labeled "Code". Click it to open the drop-down menu
- In the drop-down menu, you'll see a label "Clone with HTTPS" with a URL below it. Copy the URL by clicking the copy button
- In the CMD terminal, using the commands `dir`/`cd`, navigate to the directory where you want this repo to land
- Type ```git clone https://gitlab.com/skillnexus/reinforcement-learning/sentdexrltutorials.git``` (paste the URL from the previous steps) and press enter
- GitLab will request your username and password
    - If you do NOT have two-factor authentication enabled use your account password
    - If you do have 2FA
        - You'll need an *access token* with read_repository/write_repository permissions, use the access token as your password
        - Or you'll need to install an OAuth credential helper

### ...using SourceTree

(coming soon)

## Open this repo in [VS Code](https://code.visualstudio.com/download) as a workspace

- Open VS Code and click `File`, then `Open Workspace from File`
- Navigate to where you extracted this repo and select the file, `reinforcementlearning.code-workspace`

## Download and install [Python](https://www.python.org/downloads/release/python-3913/)

In this repo, I use [Python 3.9.13](https://www.python.org/downloads/release/python-3913/). Make sure you get the **64-bit version**.

- When you open the link, scroll down and select `Windows installer (64-bit)`

## Create a VENV for this project

*VENV* means **Virtual Environment**. It is good practice to have one virtual environment per project. By using VENVs you're effectively *isolating* your project AND your Python version and Python packages from *other* projects. The reason you want this project separation is to avoid dependency conflicts between your projects.

- In VS Code, open a terminal, make sure it is a CMD terminal
- utilizing the ```dir```/```cd``` commands, navigate to your VENV folder in your workspace folder
- type ```python -m venv ./reinforcementlearning``` and press enter
    - **WARNING:** If you have multiple versions of Python installed on your machine and want to ensure your VENV is using Python 3.9.13:
        - type ```python3.9.13 -m venv ./reinforcementlearning``` and press enter

If you want to re-do this step, navigate to the VENV folder inside the workspace directory and manually delete the VENV that you want to re-do.

## Activating the VENV you just created in a VS Code cmd terminal

- In VS Code, open a terminal, make sure it is a CMD terminal
- utilizing the ```dir```/```cd``` commands, navigate to your VENV folder in your workspace folder
- utilizing the ```dir```/```cd``` commands, navigate to the "sentdexrltutorials" folder
- utilizing the ```dir```/```cd``` commands, navigate to the "Scripts" folder
- run the "activate" script by typing ```activate``` into the terminal and pressing enter

You should see ```(reinforcementlearning)``` appear on the far left of your terminal command line, this means the virtual environment is active.

## Checking your Python version

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```python --version``` and press enter

## Checking your Pip version

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```pip --version``` and press enter

## Updating Pip to the latest version

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```python -m pip install --upgrade pip``` and press enter

Sometimes the terminal will throw an error. If you check the pip version again, as long as the latest version is returned, it's fine.

## Download and install [PyTorch](https://pytorch.org/get-started/locally/)

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118``` and press enter

Notice the command in this step is using ```pip3``` instead of just ```pip```.

## Download and install [Gymnasium](https://github.com/Farama-Foundation/Gymnasium)

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```pip install gymnasium[box2d]``` and press enter

## Download and install [Stable Baselines 3](https://stable-baselines3.readthedocs.io/en/master/guide/install.html)

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```pip install stable-baselines3[extra]``` and press enter

## Download and install [TensorFlow](https://www.tensorflow.org/install/pip)

- In VS Code, open a terminal, make sure it is a CMD terminal
- With your VENV active, type ```pip install tensorflow``` and press enter

**WARNING:** With the way we installed TensorFlow here, this is JUST to view TensorBoard. DO NOT try to run TensorFlow code with this method of installation. If you want to use TensorFlow, you'll have to follow the rest of the TensorFlow home page instructions on installing the tool properly.

## Running the code

There are more detailed steps in the experiment directories but in general...

### ...in VS Code

- In VS Code, open the command palette by clicking "View", "Command Palette" and select "Python: Select Interpreter".
- select, "Enter interpreter path..."
- select, "Find..."
- navigate to VENV -> sentdexrltutorials -> Scripts and then select, "python.exe"
- Open any Python script in VS Code and in the bottom right of the window you should see that the Python version now has a ```(reinforcementlearning)``` appended to it, this means that VS Code has "activated" the VENV similar to how you activated it in the terminal
- Open any Python script and click the play icon in the top-right of the window
    - **Warning:** Some scripts aren't meant to be run, but rather called, make sure you're running scripts that are meant to be run

You might see an error about permissions to run the script, just ignore it and VS Code should run the script eventually.

### ...in CMD/Command Line (Windows)

- Open a CMD terminal by pressing the windows key, typing "cmd" and pressing enter
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
- activate the VENV by typing ```C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate``` and pressing enter
- run a script of your choice by calling it from here
    - **Warning:** The scripts that are meant to be ran are designed to be called from the workspace directory.

## View logs by running TensorBoard

There are more detailed steps in the experiment directories but in general...

- In VS Code, open a terminal, make sure it is a CMD terminal
- utilizing the ```dir```/```cd``` commands, navigate to the folder that contains the "logs" folder, the location will depend on what you input in the [exp_2_save.py](Source/exp_2/exp_2_save.py) script
    - You may need to run the [exp_2_save.py](Source/exp_2/exp_2_save.py) script first so that the directories and log data are created
- With your VENV active, type ```tensorboard --logdir=logs``` and press enter
    - You may see a warning saying a command is deprecated, this is a bug and can safely be ignored. Actually, if you dig into the "losses.py" script, you'll find that the command that is supposedly incorrect is actually correct, like it's literally using the command that the warning is asking for, so this warning is straight up a bug
- From the terminal output, copy the web address where the tensorboard gui is located and paste it into your web browser of choice
    - Do not close this terminal, since it is literally running TensorBoard, if you want to run other scripts, you'll have to do it on a different terminal

## Generate a dependencies file to save package versions

If you want to backup all the packages your using, for example, if you fear updating and causing dependency incompatibilities...

- In VS Code, open a terminal, make sure it is a CMD terminal
- Utilizing the ```dir```/```cd``` commands, navigate to the "VENV" folder within your VS Code workspace folder
- With your VENV active, type ```pip freeze > dependencies.txt``` and press enter

Now you'll have a record of which packages DO work together, so if you update anything and it breaks, you know what to downgrade to.
