# Expense Tracker

A simple expense tracking application built in Python with a graphical user interface using Tkinter and CustomTkinter.

## Technologies Used
- Python
- Tkinter and CustomTkinter (for the user interface)
- SQLite (for local database storage)

## Description
This application allows users to track their expenses through an intuitive and easy-to-use interface created with Tkinter and CustomTkinter. The expenses data is stored locally in an SQLite database, which is initialized with a setup script included in the project.

## Features
- **Add Expenses:** Enter expense details such as date, description, category, and amount.
- **Input Validation:** User input is validated to ensure correct data format and prevent errors.
- **Delete Expenses:** Remove selected expense records from the database.
- **CRUD Operations:** Create and delete expense records easily through the GUI.
- **Monthly overview:** Monthly expenses overview, with a pie chart and a summary with the expense categories and total spending.

## Getting Started

### Prerequisites
- Python 3.x installed on your machine
- Required Python packages: `tkinter`, `customtkinter`, `CTkMessagebox`, `tkcalendar`, `sqlite3`, `matplotlib`, `seaborn`, `pillow`, `python-dateutil`, `requests`
- Standard libraries (already included with Python): tkinter, sqlite3, datetime, os, time, threading, hashlib

### Installation
1. Clone the repository:

```bash
git clone https://github.com/xKatyJane/ExpenseTracker.git
```

2. Install the required packages if you haven’t already:
```bash
pip install -r requirements.txt
```

3. Run the initial database setup script to create the SQLite database and tables.
```bash
python create_expenses_table.py
```

4. Run the main application:
```bash
python ExpenseTracker.py
```

## Screenshots

<h3 align="center">The interface with expenses added.</h3>
<p align="center">
  <img src="https://raw.githubusercontent.com/xKatyJane/ExpenseTracker/master/Assets/Screenshots/Interface_expenses.png">
</p>

<h3 align="center">Adding a new expense.</h3>
<p align="center">When clicking the ADD A NEW EXPENSE button, a new window opens, with places for data input. The data entered by the user is validated to ensure correct date format and a numerical value for the amount. The category can be chosen from the existing list or a new value can be entered. If a new category is entered, it will be added to the existing categories list.</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/xKatyJane/ExpenseTracker/master/Assets/Screenshots/Adding_new_expense_2.png">
</p>

<h3 align="center">Deleting an expense.</h3>
<p align="center">To delete an expense, select it in the table and click the DELETE EXISTING EXPENSE button. A confirmation pop-up will show, to confirm deleting the expense.</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/xKatyJane/ExpenseTracker/master/Assets/Screenshots/Deleting_an_expense.png">
</p>
