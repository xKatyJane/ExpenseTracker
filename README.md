# Expense Tracker

A simple expense tracking application built in Python with a graphical user interface using Tkinter and CustomTkinter.

## Technologies Used
- Python
- Tkinter and CustomTkinter (for the user interface)
- SQLite (for local database storage)

## Description
This application allows users to track their expenses through an intuitive and easy-to-use interface created with CustomTkinter. The expenses data is stored locally in an SQLite database, which is initialized with a setup script included in the project.

## Features
- **Add Expenses:** Enter expense details such as date, description, category, and amount.
- **Input Validation:** User input is validated to ensure correct data format and prevent errors.
- **Delete Expenses:** Remove selected expense records from the database.
- **CRUD Operations:** Create and delete expense records easily through the GUI.
- **Monthly overview:** Monthly expenses overview, with a pie chart and a summary with the expense categories and total spending.

## Getting Started

### Prerequisites
- Python 3.x installed on your machine
- Required Python packages: `customtkinter`, `sqlite3` (sqlite3 comes with standard Python installation)

### Installation
1. Clone the repository:

```bash
git clone https://github.com/yourusername/ExpenseTracker.git
```

2. Install Tkinter and CustomTkinter if you haven’t already:

```bash
pip install tkinter customtkinter
```
3. Run the initial database setup script to create the SQLite database and tables.
```bash
python create_expenses_table.py
```
4. Run the main application:
```bash
python main.py
```

## Screenshots

<h4 align="center">The interface with expenses added.</h4>
<p align="center">
  <img src="https://raw.githubusercontent.com/xKatyJane/ExpenseTracker/master/Assets/Screenshots/Interface_expenses.png">
</p>
