# OpenModelica Desktop App

This repository contains my submission for the OpenModelica Screening Task (Part 2). I've created a Python GUI application using PyQt6 to run an OpenModelica simulation executable and pass start/stop time arguments to it.

## Project Files

- `main.py`: The PyQt6 application.
- `requirements.txt`: Dependencies.
- `README.md`: Setup instructions.

## Prerequisites

1. **Python 3.6+** installed on your system.
2. The compiled OpenModelica executable for the `TwoConnectedTanks` model. 
   - Please place the compiled `.exe` (or Linux binary) and any required dependencies (like XML/DLL files) in the same directory as this repository.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akashkeote/OpenModelica.git
   cd OpenModelica
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## How to use the App

1. **Run the script**:
   ```bash
   python main.py
   ```

2. **Execute the Simulation**:
   - **Executable Path**: Use the "Browse..." button to select the OpenModelica executable you generated in Part 1.
   - **Start Time / Stop Time**: Enter the desired times as integers. 
   - Note: The app enforces the rule `0 <= Start Time < Stop Time < 5`. If you input invalid times, it will show an error message.
   - Click **Run Executable**. The app will run the simulation in the background using the `-override startTime=X,stopTime=Y` flags, so the GUI won't freeze while you wait for the results.

## Implementation Details
- The GUI is built using Object-Oriented principles by encapsulating the logic in the `OpenModelicaRunnerApp` class.
- I've strictly followed PEP8 guidelines for clean and readable code.
- To improve the user experience, I used `QProcess` to run the executable asynchronously and added error handling via `QMessageBox` popups to guide the user if something goes wrong.
