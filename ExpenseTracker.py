import tkinter as tk
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkcalendar import Calendar
import time
import os
import hashlib
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import requests
from io import BytesIO


class Adding_New_Expense_Window(ctk.CTkToplevel):
    ''' New window to add new expenses '''

    def __init__(self, expense_tracker):
        super().__init__()
        self.geometry("500x800")
        self.title("Add a new expense")
        self.grid()
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.configure(fg_color="#17202a")

        # Window title
        self.new_window_title = ctk.CTkLabel(self, text="Add a new expense", font=("Hevletica", 21), text_color="#00bcd4")
        self.new_window_title.grid(row=0, column=0, sticky="nsew")

        # Date
        self.date_label = ctk.CTkLabel(self, text="Enter the date", font=("Helvetica", 17), text_color="white")
        self.date_label.grid(row=1, column=0, sticky="sew")
        self.date_entry = ctk.CTkEntry(self, fg_color="#34495e", border_color="#00bcd4", border_width=1)
        self.date_entry.grid(row=2, column=0, sticky="nsew", padx=15, pady=15)

        self.original_calendar_icon_url ="https://raw.githubusercontent.com/xKatyJane/ExpenseTracker/master/Assets/calendar_icon.png"
        self.response_calendar_icon = requests.get(self.original_calendar_icon_url)
        self.calendar_icon_data = BytesIO(self.response_calendar_icon.content)
        self.calendar_icon = Image.open(self.calendar_icon_data).resize((40,40))
        self.calendar_icon_tk = ImageTk.PhotoImage(self.calendar_icon)
        self.date_button = ctk.CTkButton(self, text="", image=self.calendar_icon_tk, fg_color="#00bcd4", width=50, command=self.open_calendar)
        self.date_button.grid(row=2, column=0, sticky="nse", padx=15, pady=15)

        # Description
        self.description_label = ctk.CTkLabel(self, text="Enter the description", font=("Helvetica", 17), text_color="white")
        self.description_label.grid(row=3, column=0, sticky="sew")
        self.description_entry = ctk.CTkEntry(self, fg_color="#34495e", border_color="#00bcd4", border_width=1)
        self.description_entry.grid(row=4, column=0, sticky="nsew", padx=15, pady=15)

        # Category
        categories = expense_tracker.retrieve_categories()
        self.category_label = ctk.CTkLabel(self, text="Select or add a category", font=("Helvetica", 17), text_color="white")
        self.category_label.grid(row=5, column=0, sticky="sew")
        self.category_combobox = ctk.CTkComboBox(self, values=categories,  fg_color="#34495e", border_color="#00bcd4", border_width=1, button_color="#00bcd4")
        self.category_combobox.grid(row=6, column=0, sticky="nsew", padx=15, pady=15)
        self.category_combobox.set("")

        # Amount
        self.amount_label = ctk.CTkLabel(self, text="Enter the amount", font=("Helvetica", 17), text_color="white")
        self.amount_label.grid(row=7, column=0, sticky="sew")
        self.amount_entry = ctk.CTkEntry(self, fg_color="#34495e", border_color="#00bcd4", border_width=1)
        self.amount_entry.grid(row=8, column=0, sticky="nsew", padx=15, pady=15)

        self.expense_added = ctk.CTkLabel(self, text=" ", font=("Helvetica", 17), text_color="green")
        self.expense_added.grid(row=9, column=0, sticky="sew")

        # Sbmit button
        self.submit_expense_button = ctk.CTkButton(self, text="Submit", fg_color="#6600FF", font=("Helvetica", 17), command=self.validate_and_submit_user_input)
        self.submit_expense_button.grid(row=10, column=0, sticky="ns", padx=15, pady=15)

        self.calendar_window = None

    def open_calendar(self):
        ''' Opens a calendar in a new window to pick a date '''

        # Prevent opening more that one calendar window at the same time
        if self.calendar_window and self.calendar_window.winfo_exists():
            return

        # Calendar window configuration
        self.calendar_window = tk.Toplevel(self)
        self.calendar_window.title("Select Date")
        self.calendar_window.geometry("300x300")
        self.calendar_window.grid()
        self.calendar_window.rowconfigure(0, weight=4, uniform="a")
        self.calendar_window.rowconfigure(1, weight=1, uniform="a")
        self.calendar_window.columnconfigure(0, weight=1, uniform="a")
        self.calendar_window.configure(background="#17202a")

        # The Calendar widget
        self.calendar = Calendar(self.calendar_window, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 14),
                                 background="#17202a", foreground="#00bcd4",
                                 selectforeground="white", selectbackground="#6600FF", headersbackground="#00bcd4",
                                 normalforeground="white", weekendforeground="#b2ebf2", bordercolor="#00bcd4",
                                 normalbackground="#34495e", weekendbackground="#34495e", othermonthbackground="#34495e", othermonthwebackground="#34495e")
        self.calendar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # The Confirm button
        confirm_date_button = ctk.CTkButton(self.calendar_window, text="Confirm Date", fg_color="#6600FF", command=self.get_date)
        confirm_date_button.grid(row=1, column=0, sticky="ns", padx=15, pady=15)

    def get_date(self):
        ''' Fetches selected date and updates the label in the Add_New_Expense_Window '''

        selected_date = self.calendar.get_date()
        self.date_entry.delete(0, ctk.END)
        self.date_entry.insert(0, selected_date)
        self.calendar_window.destroy()

    def validate_and_submit_user_input(self):
        ''' Validates that data is in the correct format and saves the data to the DB file  '''

        # Get the data from the user inputs
        expense_date = self.date_entry.get()
        expense_description = self.description_entry.get().capitalize()
        expense_category = self.category_combobox.get().capitalize()
        expense_amount = self.amount_entry.get()

        # Validate if all fields are filled
        if not expense_date or not expense_description or not expense_category or not expense_amount:
            messagebox.showerror("Error", "All fields must be filled.")
            return
        # Validate date format
        try:
            expense_date_datetime = datetime.strptime(expense_date, '%Y-%m-%d').date()
        except:
            messagebox.showerror("Error", "Not a valid date format, use YYYY-MM-DD")
            return
        # Validate amount
        try:
            expense_amount = float(expense_amount)
            if expense_amount <= 0:
                return
        except:
            messagebox.showerror("Error", "Not a valid number")
            return

        # Insert new values into database
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (Date, Description, Category, Amount) VALUES (?, ?, ?, ?)", (expense_date, expense_description, expense_category, expense_amount))
        conn.commit()

        # Display success message and clear entry fields
        success_message = CTkMessagebox(message="Operation successful!", icon="check", option_1="OK")
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.category_combobox.set('')
        self.amount_entry.delete(0, tk.END)

        # Update categories list
        cur.execute("SELECT DISTINCT Category from expenses")
        updated_categories = [row[0] for row in cur.fetchall()]
        conn.close()
        self.category_combobox.configure(values=updated_categories)


class Expense_Tracker(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Expense Tracker")
        self.geometry("1200x1000")
        self.grid()
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform="a")
        self.configure(fg_color="#17202a")
        self.toplevel_window = None

        # Widgets and functions
        self.recent_expenses()
        self.define_current_month()
        self.retrieve_data(month, year)
        self.populate_table(current_table_data)
        self.expense_summary()
        self.define_hashlib()
        self.update_pie_chart_and_summary(month, year)
        
        # Threading
        threading.Thread(target=self.check_for_updates, args=(current_hash, month, year), daemon=True).start()


    def expense_summary(self):
        ''' Defines the configuration of the left side of the main interface '''

        # Frame
        self.left_frame = ctk.CTkFrame(self, fg_color="#17202a")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid()
        self.left_frame.rowconfigure(0, weight=1, uniform="a")
        self.left_frame.rowconfigure(1, weight=5, uniform="a")
        self.left_frame.rowconfigure(2, weight=4, uniform="a")
        self.left_frame.columnconfigure(0, weight=1, uniform="a")

        # Frame for the current month and two buttons (previous and next month)
        self.button_frame = ctk.CTkFrame(self.left_frame, fg_color="#17202a")
        self.button_frame.grid(row=0, column=0, sticky="nsew")
        self.button_frame.rowconfigure(0, weight=1, uniform="a")
        self.button_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")

        # Label to display the currenth month and year
        self.show_current_month = ctk.CTkLabel(self.button_frame, text="", font=("Helvetica", 18))
        self.show_current_month.grid(row=0, column=1)

        # Previous and next month buttons
        self.previous_month_button = ctk.CTkButton(self.button_frame, text="Previous\nmonth", fg_color="#6600FF", font=("Helvetica", 14), command=lambda: self.retrieve_previous_month(current_month_str))
        self.previous_month_button.grid(row=0, column=0, sticky="nsew", padx=20, pady=18)
        self.next_month_button = ctk.CTkButton(self.button_frame, text="Next\nmonth", fg_color="#6600FF", font=("Helvetica", 14), command=lambda: self.retrieve_next_month(current_month_str))
        self.next_month_button.grid(row=0, column=2, sticky="nsew", padx=20, pady=18)

        # Monthly categories summary
        self.monthly_summary = ctk.CTkFrame(self.left_frame, fg_color="#17202a")
        self.monthly_summary.grid(row=2, column=0, sticky="nsew")
        self.monthly_summary.rowconfigure(0, weight=1, uniform="a")
        self.monthly_summary.rowconfigure(1, weight=12, uniform="a")
        self.monthly_summary.columnconfigure((0, 1), weight=1, uniform="a")

        current_table_data, categories_list, totals_list = self.retrieve_data(month, year)

        # Monthly total expenses
        self.monthly_totals = ctk.CTkLabel(self.monthly_summary, text=f"Total monthly expenses: {sum(totals_list)} €", font=("Montserrat", 19, "bold"), text_color="#00bcd4")
        self.monthly_totals.grid(row=0, column=0, columnspan=2)

        # Expenses by category
        categories_text= "\n".join(categories_list)
        self.category_names = CTkLabel(self.monthly_summary, text=categories_text, font=("Georgia", 18), justify="right", anchor="ne")
        self.category_names.grid(row=1, column=0, sticky="nsew", padx=20, pady=(20,0))

        totals_str = [str(item)+" €" for item in totals_list]
        totals_text= "\n".join(totals_str)
        self.totals = CTkLabel(self.monthly_summary, text=totals_text, font=("Georgia", 18), justify="left", anchor="nw")
        self.totals.grid(row=1, column=1, sticky="nsew", padx=20, pady=(20,0))

        # Pie chart
        plt.style.use("seaborn-v0_8-deep")
        self.fig, self.ax = plt.subplots(facecolor='#17202a')
        self.ax.set_facecolor('#17202a')
        self.pie_chart_canvas = FigureCanvasTkAgg(self.fig, self.left_frame)
        self.pie_chart_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self.update_pie_chart_and_summary(month, year)


    def update_pie_chart_and_summary(self, month, year):
        ''' Updates the main chart and spending by category '''
        global current_month_str

        # Canvas and the pie chart
        current_table_data, categories_list, totals_list = self.retrieve_data(month, year)
        self.monthly_totals.configure(text=f"Total monthly expenses: {sum(totals_list)}")

        # Expenses by category
        categories_text= "\n".join(categories_list)
        self.category_names.configure(text=categories_text)
        totals_str = [str(item)+" €" for item in totals_list]
        totals_text= "\n".join(totals_str)
        self.totals.configure(text=totals_text)

        # Pie chart
        categories_list_modified = [list_item.replace(" ", "\n") for list_item in categories_list]
        self.ax.clear()
        self.ax.pie(totals_list, labels=categories_list_modified, autopct='%1.1f%%', radius=1.1, labeldistance=1.1, pctdistance=0.6, startangle=90,
               textprops={"fontfamily" : "Helvetica" ,"fontsize" : 6, "color" : "white"})
        circle = plt.Circle(xy=(0,0), radius=.85, facecolor="#17202a")
        plt.gca().add_artist(circle)
        self.fig.suptitle("Total expenses by category", fontfamily="Helvetica", fontsize=8, color="#00bcd4")
        self.pie_chart_canvas.draw()

        # Displaying name of the current month
        current_month_str = month + " " + year
        date_object = datetime.strptime(current_month_str, "%m %Y")
        formatted_date = date_object.strftime("%B %Y")
        self.show_current_month.configure(text=formatted_date)

        return current_month_str


    def recent_expenses(self):
        ''' Defines the confguration for the main window - expenses table '''
        global expenses_table

        # Right frame - configuration
        self.main_window = ctk.CTkFrame(self, fg_color="#17202a")
        self.main_window.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.main_window.columnconfigure(0, weight=1, uniform="a")
        self.main_window.rowconfigure((0,1), weight=1, uniform="a")
        self.main_window.rowconfigure(2, weight=8, uniform="a")

        # Title, button - configuration
        self.main_title = ctk.CTkLabel(self.main_window, text="Monthly expenses", font=("Raleway", 24, "bold"), text_color="#00bcd4", bg_color="#17202a")
        self.main_title.grid(row=0, column=0, sticky="nsew")
        self.two_buttons_frame = ctk.CTkFrame(self.main_window, fg_color="#17202a")
        self.two_buttons_frame.grid(row=1, column=0, sticky="nsew")
        self.two_buttons_frame.columnconfigure((0, 1), weight=1, uniform="a")
        self.two_buttons_frame.rowconfigure(0, weight=1, uniform="a")

        self.new_expense_button = ctk.CTkButton(self.two_buttons_frame, text="Add a new expense",
                                                fg_color="#6600FF", width=90, height=50,
                                                font=("Helvetica", 17), command=self.open_new_window)
        self.new_expense_button.grid(row=0, column=0)

        self.delete_expenses_button = ctk.CTkButton(self.two_buttons_frame, text="Delete existing expense",
                                                fg_color="#6600FF", width=90, height=50,
                                                font=("Helvetica", 17), command=self.delete_record)
        self.delete_expenses_button.grid(row=0, column=1)

        # Scrollable frame for the table - configuration
        self.table_frame = ctk.CTkScrollableFrame(self.main_window, fg_color="#17202a")
        self.table_frame.grid(row=2, column=0, sticky="nsew")
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)

        # Expenses table - configuration
        expenses_table = ttk.Treeview(self.table_frame, columns=("date", "description", "category", "amount"),
                                      show="headings", selectmode = "extended", padding=(0,20))
        expenses_table.heading("date", text="Date")
        expenses_table.heading("description", text="Description")
        expenses_table.heading("category", text="Category")
        expenses_table.heading("amount", text="Amount")
        expenses_table.grid(sticky="nsew")
        style = ttk.Style()

        # Table styling
        style = ttk.Style()
        style.theme_use("clam")
        expenses_table.tag_configure('evenrow', background="#34495e")
        expenses_table.tag_configure('oddrow', background="#17202a")
        style.configure("Treeview", background="#34495e", font=("Helvetica", 17), rowheight=55,
                        borderwidth=1, relief="solid", fieldbackground="#17202a",
                        foreground="white", padding=(50, 20))
        
        # Table headings
        style.configure("Treeview.Heading", font=("Helvetica", 18), foreground="#00bcd4", background="black",
                        padding=(20,20), borderwidth=0, relief="solid")

        style.configure("Treeview.Heading", font=("Helvetica", 18), foreground="#00bcd4", background="black",
                        padding=(20,20), borderwidth=0, relief="solid")
        
        style.map("Treeview",
          background=[('selected', '#00bcd4')],
          foreground=[('selected', 'black')])


    def define_current_month(self):
        ''' Fetches the current month for the initial display '''
        global month, year

        month = datetime.now().strftime("%m")
        year = str(datetime.now().year)
        return month, year
    

    def month_being_displayed(self, current_month_str):
        ''' Fetches the month being displayed, to ensure the correct month being dispalyed on updating the data '''

        global month, year
        month = current_month_str.split()[0]
        year = current_month_str.split()[1]
        return month, year


    def retrieve_data(self, month, year):
        ''' Retrieves data from the SQL DB file'''
        global current_table_data, categories_list, totals_list

        # Retrieve data from the DB file
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ? ORDER BY Date DESC", (month, year))
        column_names = list(map(lambda x: x[0], cur.description))[1:]
        current_table_data = cur.fetchall()

        cur.execute("""SELECT Category, SUM(Amount) FROM expenses
                    WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                    GROUP BY Category ORDER BY Amount DESC LIMIT 12""", (month, year))
        category_sum_tuples = cur.fetchall()
        category_sum_tuples = sorted(category_sum_tuples, key=lambda x: x[1], reverse=True)
        categories_list = [row[0] for row in category_sum_tuples]
        totals_list = [float(row[1]) for row in category_sum_tuples]
        conn.close()
        return current_table_data, categories_list, totals_list


    def retrieve_categories(self):
        ''' Retrieves categories, to update the list of available categories instantly '''
        global categories

        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT Category from expenses")
        categories = [row[0] for row in cur.fetchall()]
        conn.close()
        return categories


    def populate_table(self, current_table_data):
        ''' Populates the table with the fetched data'''

        # Clear previous data
        for row in expenses_table.get_children():
            expenses_table.delete(row)

        # Insert new data, alterate colors of the rows
        for idx, row in enumerate(current_table_data):
            row_displayed_values = row[1:]
            row_id = row[0]
            row_values = expenses_table.insert(parent="", index=0, iid=row_id, values=row_displayed_values)
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            expenses_table.item(row_values, tags=(tag,))


    def define_hashlib(self):
        ''' Defines the initial hash, to be able to monitor file changes '''
        global current_hash

        with open ("expenses.db", "rb") as file:
            file_content = file.read()
            current_hash = hashlib.sha256(file_content).hexdigest()


    def check_for_updates(self, current_hash, month, year):
        ''' A background function that runs as a daemon thread, continuously monitoring if there have been file changes '''

        while True:
            with open ("expenses.db", "rb") as file:
                file_content = file.read()
                new_hash = hashlib.sha256(file_content).hexdigest()
            if new_hash == current_hash:
                continue
            else:
                month, year = self.month_being_displayed(current_month_str)
                current_table_data, categories_list, totals_list = self.retrieve_data(month, year)
                self.populate_table(current_table_data)
                self.update_pie_chart_and_summary(month, year)
            current_hash = new_hash
            time.sleep(2)


    def retrieve_previous_month(self, current_month_str):
        ''' Activated on clicking PREVIOUS MONTH button '''

        current_month = current_month_str
        current_month_datetime = datetime.strptime(current_month, "%m %Y")
        previous_month_datetime = current_month_datetime - relativedelta(months=1)
        month = previous_month_datetime.strftime("%m")
        year = previous_month_datetime.strftime("%Y")
        previous_month_str = month + " " + year
        self.retrieve_data(month, year)
        self.populate_table(current_table_data)
        self.update_pie_chart_and_summary(month, year)


    def retrieve_next_month(self, current_month_str):
        ''' Activated on clicking NEXT MONTH button '''

        current_month = current_month_str
        current_month_datetime = datetime.strptime(current_month, "%m %Y")
        next_month_datetime = current_month_datetime + relativedelta(months=1)
        month = next_month_datetime.strftime("%m")
        year = next_month_datetime.strftime("%Y")
        next_month_str = month + " " + year
        self.retrieve_data(month, year)
        self.populate_table(current_table_data)
        self.update_pie_chart_and_summary(month, year)


    def delete_record(self):
        selected = expenses_table.selection()
        delete_confirmation = CTkMessagebox(title="Are you sure?", message="Do you want to delete selected row?", icon="question",
                                            option_1="Cancel", option_2="No", option_3="Yes")
        response = delete_confirmation.get()
        if response == "No":
            pass
        elif response == "Cancel":
            pass
        elif response == "Yes":
            for item in selected:
                row_data = expenses_table.item(item, "values") 
                row_id = selected[0]
                conn = sqlite3.connect("expenses.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM expenses WHERE ID = ?", (row_id,))
                conn.commit()
                conn.close()


    def open_new_window(self):
        ''' Ensures that only one top level window (add new expenses window) is open at the same time '''

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Adding_New_Expense_Window(self)
        else:
            self.toplevel_window.focus()


if __name__ == "__main__":
    app = Expense_Tracker()
    app.mainloop()