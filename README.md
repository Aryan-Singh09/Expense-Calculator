💰 Smart Expense Manager (Enhanced):

A versatile, multi-mode expense tracking application built in Python. This tool allows users to record daily expenses and provides insights and data visualization through either a modern Desktop GUI or a simple Web Interface.

✨ Features
Dual Interface: Run as a standalone Desktop application (using customtkinter) or as a local Web application (using Flask).

Expense Tracking: Easily input Date, Category, and Amount for every transaction.

Data Persistence: All expense records are automatically saved to an expenses.csv file, ensuring data is kept between sessions.

Data Visualization (GUI Mode): Generate interactive Bar Charts and Pie Charts of spending by category using matplotlib.

AI Insights: Get simple rule-based advice on spending patterns and budget monitoring.

🛠️ Installation and Setup
Prerequisites
You need Python 3.x installed on your system.

Dependencies
This project requires a few external libraries for both the GUI and Web modes. Install them using pip:

pip install customtkinter matplotlib flask

🚀 How to Run
The application can be launched in one of two modes: GUI (Desktop) or Web (Browser).

1. Desktop GUI Mode (Recommended for Local Use)
This mode provides the full feature set, including interactive charts. Run the script with the gui flag (or run without any argument, as gui is the default).

python Expense-Calculator.py gui
# OR
python Expense-Calculator.py

2. Web Mode (Browser Access)
This mode runs a local server for browser-based access.

python Expense-Calculator.py web

The application will start a local Flask server, typically accessible at http://127.0.0.1:5000.

📂 File Structure
Expense-Calculator.py: The main application file containing all the logic for data handling, GUI, and web modes.

expenses.csv: This file is automatically created on first run and stores all your expense data in CSV format (Date,Category,Amount).
