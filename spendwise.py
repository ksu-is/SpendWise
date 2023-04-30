import sqlite3

#Function to initialize a database
def init():
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string
        )
    '''
    cur.execute(sql)
    conn.commit()
    
    # Call the init() function to create the expenses table
init()

#Fuction to record expenses to the database
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

#Function to view expenses based on a specific category or month/day
def view(category, date):
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    if category.isalpha():
        sql = '''
        select * from expenses where category = '{}' and date like '{}%'
        '''.format(category, date)
        sql2 = '''
        select sum(amount) from expenses where category = '{}' and date like '{}%'
        '''.format(category, date)
    else:
        sql = '''
        select * from expenses where date like '{}%'
        '''.format(date)
        sql2 = '''
        select sum(amount) from expenses where date like '{}%'
        '''.format(date)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    for expense in results:
        print(expense)
    print('\nTotal:','$' + str(total_amount))

#Fuction for comparing current months spending to a month selected by the user
def compare(comp_month):
    from datetime import date
    month = date.today().strftime("%Y-%m")
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    select sum(amount) from expenses where date like'{}%'
    '''.format(month)
    sql2 = '''
    select sum(amount) from expenses where date like'{}%'
    '''.format(comp_month)
    cur.execute(sql)
    month_amount = cur.fetchone()[0]
    cur.execute(sql2)
    comp_month_amount = cur.fetchone()[0]
    if comp_month_amount == None:
        print('\nNo expenses recorded for that month')
    elif month_amount > comp_month_amount:
        percent = ((month_amount / comp_month_amount) - 1) * 100
        print('\nSo far your spending is already up',str(percent) + '% this month compared to', comp_month)
    elif month_amount == comp_month_amount:
        print('\nSo far you have the spent the same amount of money this month')
    else:
        percent = (1 - (month_amount / comp_month_amount)) * 100
        print('\nSo far your spending is down',str(percent) + '% this month compared to', comp_month)
def analysis():
    conn = sqlite3.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    select * from expenses
    '''.format(tracker)
    sql2 = '''
    select sum(amount) from expenses
    '''.format(tracker)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    for expense in results:
        print(expense)
    print('\nTotal:','$' + str(total_amount))
    newbudget = int(total)- int(total_amount)  
    print("Your new balance is $", newbudget)
    if int(total_amount) > int(total):
        print ("You are under budget. Please save your money or else you will go bankrupt! I am serious")
    if int(newbudget) > 0 and int(newbudget) < 500:
        print("You are under $500, please try to save more money")
    elif int(newbudget) > 500 and int(newbudget) < 1000:
        print("Your balance is more than $ 500. You are doing great. Try to save more  :) ")
    elif int(newbudget) > 1000 and int(newbudget) < 1500:
        print("Your balance is more than $ 1000. You are doing great. Try to save more  :) ") 
    elif int(newbudget) > 1500 and int(newbudget) < 2000:
        print("Your balance is more than $ 1500. You are doing great. Try to save more  :) ")
    elif int(newbudget) > 2000 and int(newbudget) < 2500:
        print("Your balance is more than $ 2000. You are doing great. Try to save more  :) ")
    elif int(newbudget) > 2500 :
        print("Your balance is more than $ 2500. You are doing great. Try to save more  :) ")
    else:
        print() 
        
# Function to calculate savings required to reach financial goals
def savings_calculator(budget):
    #call init function
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
        
        
        
#Welcome message
print("\nWelcome to MyMoney Expense Tracker!")
print("This app allows you to record and view your spending habits to help you become a more conscious spender!")
 
#Main loop for user input
total= input("What is your current total budget?\n:")
while True:
        print("\nWhat would you like to do?")
        print("1 - Initialize an expense database(only do this once)\n2 - Enter an expense\n3 - View expenses based on date and category\n4 - Compare Month\n5 - Check Balance\n6 - Update balance\nQ - Quit")
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
        elif ans.lower() == "q":
            print('Goodbye!\n')
            break
