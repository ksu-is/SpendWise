import sqlite3

# Function to initialize a database
def init():
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()

    # Create expenses table if it doesn't exist
    sql_expenses = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string
        )
    '''
    cur.execute(sql_expenses)

    


# Call the init() function to create the expenses table and category_budgets table
init()

# ... rest of the code ...


# Function to record expenses to the database
def log(amount, category, message=""):
    from datetime import datetime
    date = str(datetime.now())
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    insert into expenses values (
        {},
        '{}',
        '{}',
        '{}'
          )
    '''.format(amount, category, message, date)
    try:
        cur.execute(sql)
        conn.commit()
        print('\nExpense saved!\n')
    except:
        print('\nExpense not saved. Please try again and do not punctuate the category or detailed message.\n')

# Function to view expenses based on a specific category or month/day
def view(category="", date=""):
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    if category.isalpha():
        sql = '''
        select * from expenses where category = '{}' and date like '{}%'
        '''.format(category, date)
        sql2 = '''
        select sum(amount) from expenses where category = '{}' and date like '{}%'
        '''.format(category, date)
        sql3 = '''
        select budget from category_budgets where category = '{}'
        '''.format(category)
    else:
        sql = '''
        select * from expenses where date like '{}%'
        '''.format(date)
        sql2 = '''
        select sum(amount) from expenses where date like '{}%'
        '''.format(date)
        sql3 = None

    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]

    if sql3 is not None:
        cur.execute(sql3)
        category_budget = cur.fetchone()
        if category_budget is not None:
            category_budget = category_budget[0]
            remaining_budget = category_budget - total_amount
            print(f'\nRemaining budget for {category}: ${remaining_budget}')

    for expense in results:
        print(expense)
    print('\nTotal:','$' + str(total_amount))


# Function to calculate savings required to reach financial goals
def savings_calculator(budget):
    #NEW NEW NEW
    init()  
    from datetime import date
    month = date.today().strftime("%Y-%m")
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    select sum(amount) from expenses where date like'{}%'
    '''.format(month)
    cur.execute(sql)
    month_amount = cur.fetchone()[0]
    if month_amount is None:
        month_amount = 0
    savings_required = float(budget) - month_amount
    print("To reach your financial goal, you need to save $", savings_required, "per month.")





#NEW FEATURE: IMPLEMENT A BUDGETING CATEGORY
#this will create a new table in the database to store the category budgets
sql_category_budget = '''
create table if not exists category_budgets (
    category string primary key,
    budget number
    )
'''


#create function to set, update and view category budgets
def set_category_budget(category, budget):
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    
    # Check if category_budgets table exists, if not, create it
    sql_create = '''
    create table if not exists category_budgets (
        category string primary key,
        budget number
    )
    '''
    cur.execute(sql_create)
    conn.commit()
    
    # Insert or update the category budget
    sql_insert_update = '''
    insert or replace into category_budgets (category, budget)
    values (?, ?)
    '''
    cur.execute(sql_insert_update, (category, budget))
    conn.commit()

    print(f"Budget for {category} has been set to ${budget}")


def view_category_budgets():
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    select * from category_budgets
    '''
    cur.execute(sql)
    results = cur.fetchall()
    for budget in results:
        print(f'{budget[0]}: ${budget[1]}')

import csv

def export_data_to_csv(filename):
    import csv

    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    results = cur.fetchall()

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["amount", "category", "message", "date"])

        for expense in results:
            csv_writer.writerow(expense)

    print(f"Data exported to {filename} successfully.")

def import_data_from_csv(filename):
    import csv

    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()

    # Read expenses from the CSV file
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            amount, category, message, date = row
            sql = '''
            INSERT INTO expenses (amount, category, message, date)
            VALUES (?, ?, ?, ?)
            '''
            cur.execute(sql, (amount, category, message, date))

    conn.commit()
    print(f"Data imported from {filename}")


    # Read expenses from the CSV file
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            amount, category, message, date = row
            sql = '''
            INSERT INTO expenses (amount, category, message, date)
            VALUES (?, ?, ?, ?)
            '''
            cur.execute(sql, (amount, category, message, date))

    conn.commit()
    print(f"Data imported from {filename}")


    # Fetch all expenses
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    # Write expenses to a CSV file
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['amount', 'category', 'message', 'date'])
        for expense in expenses:
            writer.writerow(expense)

    print(f"Data exported to {filename}")

# Welcome message
print("\nManage your expenses easily and save smarter with our intuitive software. Let's get started!")
print("This app allows you to record and view your spending habits to help you become a more conscious spender!")

#Main loop for user input
total= input("What is your current total budget?\n:")
while True:
        print("\nWhat would you like to do?")
        print("1 - Initialize an expense database (only do this once)\n2 - Enter an expense\n3 - View expenses based on date and category\n4 - Compare Month\n5 - Check Balance\n6 - Update balance\n7 - Calculate Savings Required\n8 - Set Category Budget\n9 - View Category Budgets\n10 - Export Data to CSV\n11 - Import Data from CSV\nQ - Quit")
        ans = input(":")
        print()

        if ans == "1":
            init()
            print('Database initialized')
        elif ans == "2":
            cost = input('What is the amount of the expense?\n:')
            cat = input('What is the category of the expense?\n1 - Food\n2 - Entertainment\n3 - Education\n4 - Travel\n5 - Car\n6 - Utilities\n7 - Insuranece\n8 - Other\n:').title()
            msg = input('What is the expense for?\n:')
            log(cost,cat,msg)
        elif ans == "3":
            date = input('What month or day do you want to view? (yyyy-mm or yyyy-mm-dd)\n:')
            category = input('Enter what category of expenses you would like to view or press enter to view all\n:').title()
            print()
            view(category,date)
        elif ans == "4":
            comp_month = input('\nWhat month would you like to compare this months spending to? (yyyy-mm)\n:')
            compare(comp_month)
        elif ans == "5":
            tracker= ""
            analysis()
        elif ans == "6":
            total= input("What is your new balance?\n:")
            if total.isnumeric():
                print("You now have $ ", total)
            else:
                total=input("Only in numbers please, \nWhat is your new balance?\n:")
        elif ans == "7":
            savings_calculator(total)
        
        elif ans == "8":
            cat = input('What is the category for which you want to set a budget?\n1 - Food\n2 - Entertainment\n3 - Education\n4 - Travel\n5 - Car\n6 - Utilities\n7 - Insurance\n8 - Other\n:').title()
            budget = input(f'What is the budget for {cat}?\n:')
            set_category_budget(cat, budget)
        elif ans == "9":
            print('\nCategory Budgets:')
            view_category_budgets()

        elif ans == "10":
            filename = input("Enter the name of the CSV file you want to export data to (e.g., expenses.csv):\n")
            export_data_to_csv(filename)

        elif ans == "11":
            filename = input("Enter the name of the CSV file you want to import data from (e.g., expenses.csv):\n")
            import_data_from_csv(filename)

        elif ans.lower() == "q":
            print('Goodbye!\n')
            break



