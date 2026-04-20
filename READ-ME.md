# TaskFlow Pro: SQLite B-Tree Indexing Demo

## Requirements
Ensure you have Python 3.8+ installed on your machine.

## Setup Instructions
1. Download and extract this project folder to your computer.
2. Open a terminal instance **specifically inside this project folder**. You can do this in a few ways:
   * **Code Editor:** Open the entire folder in VS Code or Cursor and open a new Integrated Terminal.
   * **Windows:** Open the folder in File Explorer, click the file path bar at the top, type `cmd`, and hit Enter.
   * **Mac:** Right-click the folder in Finder and select "New Terminal at Folder".
3. Once your terminal is open inside the project root, install the required dependencies by running:
   `python -m pip install -r requirements.txt`

## How to Run the Application
1. In that same terminal, launch the Streamlit dashboard by running:
   `python -m streamlit run app.py`
2. The application will automatically open in your default web browser at `http://localhost:8501`.

## Included Files
* `app.py`: The main application code and UI dashboard.
* `tasks_pro.db`: The SQLite database containing a synthetic dataset to demonstrate the B-Tree index functionality.
* `requirements.txt`: The library dependencies.