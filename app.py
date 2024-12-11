


from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_database():
    try:
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            User_ID INTEGER PRIMARY KEY,
            Email TEXT UNIQUE,
            Password TEXT,
            Role TEXT
        )
        ''')
        
        # Create Bank table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bank (
            Bank_ID INTEGER PRIMARY KEY,
            Bank_Name TEXT,
            Address TEXT
        )
        ''')
        
        # Create Branch table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Branch (
            Branch_ID INTEGER PRIMARY KEY,
            Branch_Name TEXT,
            Address TEXT,
            Bank_ID INTEGER,
            FOREIGN KEY (Bank_ID) REFERENCES Bank(Bank_ID)
        )
        ''')
        
        # Create Customer table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            Customer_ID INTEGER PRIMARY KEY,
            First_Name TEXT,
            Last_Name TEXT,
            DOB DATE,
            Contact_NO_1 TEXT,
            Contact_NO_2 TEXT,
            Landline_No TEXT,
            Email TEXT UNIQUE,
            Age INTEGER,
            Address TEXT,
            Bank_ID INTEGER,
            FOREIGN KEY (Bank_ID) REFERENCES Bank(Bank_ID)
        )
        ''')
        
        # Create Employee table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            Employee_ID INTEGER PRIMARY KEY,
            Ename TEXT,
            DOB DATE,
            Age INTEGER,
            Salary DECIMAL(10, 2),
            Contact_NO_1 TEXT,
            Contact_NO_2 TEXT,
            Landline_No TEXT,
            Address TEXT,
            Email TEXT UNIQUE,
            Branch_ID INTEGER,
            FOREIGN KEY (Branch_ID) REFERENCES Branch(Branch_ID)
        )
        ''')
        
        # Create Customer_Account table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer_Account (
            Customer_ID INTEGER,
            Account_No INTEGER,
            PRIMARY KEY (Customer_ID, Account_No),
            FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
            FOREIGN KEY (Account_No) REFERENCES Account(Account_No)
        )
        ''')
        
     
        # Create Transaction table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Transaction" (
            Transaction_ID INTEGER PRIMARY KEY,
            Amount DECIMAL(10, 2),
            Date DATE,
            Sender_ID INTEGER,
            Receiver_ID INTEGER,
            Account_No INTEGER,
            FOREIGN KEY (Account_No) REFERENCES Account(Account_No)
        )
        ''')
        
        # Create Account table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            Account_No INTEGER PRIMARY KEY,
            Account_Type TEXT,
            Balance DECIMAL(10, 2),
            Since DATE,
            Customer_ID INTEGER,
            FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
        )
        ''')
        
        # Create Customer_Account table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer_Account (
            Customer_ID INTEGER,
            Account_No INTEGER,
            PRIMARY KEY (Customer_ID, Account_No),
            FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
            FOREIGN KEY (Account_No) REFERENCES Account(Account_No)
        )
        ''')
        
        # Create Account_Transaction table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account_Transaction (
            Account_No INTEGER,
            Transaction_ID INTEGER,
            PRIMARY KEY (Account_No, Transaction_ID),
            FOREIGN KEY (Account_No) REFERENCES Account(Account_No),
            FOREIGN KEY (Transaction_ID) REFERENCES "Transaction"(Transaction_ID)
        )
        ''')
        
        with sqlite3.connect('bank.db') as conn:
            conn.execute('DROP TABLE IF EXISTS Loan')
            conn.execute('''
            CREATE TABLE Loan (
            Loan_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_ID INTEGER,
            Amount REAL,
            Purpose TEXT,
            Status TEXT,
            Issue_date DATE,
            Due_date DATE,
            FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
            )
        ''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Logging for debugging
        print(f"Attempting login for username: {username}")

        cursor.execute('SELECT * FROM Users WHERE Email = ? AND Password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['role'] = user[3]
            
            if user[3] == 'customer':
                cursor.execute('SELECT First_Name FROM Customer WHERE Email = ?', (username,))
                customer = cursor.fetchone()
                if customer:
                    session['first_name'] = customer[0]
                    return jsonify({"message": "Login successful", "redirect_url": url_for('customer_dashboard')})
                else:
                    print(f"Customer not found for email: {username}")
                    return jsonify({"message": "Customer data not found"}), 404
            elif user[3] == 'employee':
                cursor.execute('SELECT Ename FROM Employee WHERE Email = ?', (username,))
                employee = cursor.fetchone()
                if employee:
                    session['employee_name'] = employee[0]
                    return jsonify({"message": "Login successful", "redirect_url": url_for('employee_dashboard')})
                else:
                    print(f"Employee not found for email: {username}")
                    return jsonify({"message": "Employee data not found"}), 404
            else:
                return jsonify({"message": "Invalid role"}), 401
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    except Exception as e:
        print(f"An error occurred during login: {e}")
        return jsonify({"message": f"An error occurred: {e}"}), 500



@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        dob = data.get('dob')
        contact1 = data.get('contact1')
        contact2 = data.get('contact2')
        landline = data.get('landline')
        email = data.get('email')
        age = data.get('age')
        address = data.get('address')
        bank_id = data.get('bank_id')

        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Insert new customer
            cursor.execute('''
                INSERT INTO Customer (First_Name, Last_Name, DOB, Contact_NO_1, Contact_NO_2, Landline_No, Email, Age, Address, Bank_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, dob, contact1, contact2, landline, email, age, address, bank_id))
            customer_id = cursor.lastrowid
            
            # Insert into Users table
            cursor.execute('INSERT INTO Users (Email, Password, Role) VALUES (?, ?, ?)', (email, password, 'customer'))
            
            # Create an associated account for the new customer with initial balance of 5000
            cursor.execute('INSERT INTO Account (Account_Type, Balance, Since, Customer_ID) VALUES (?, ?, ?, ?)', ('Savings', 5000, datetime.date.today(), customer_id))
            
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Customer registered successfully"}), 200
        except sqlite3.IntegrityError:
            return jsonify({"message": "Email already exists"}), 400
        except Exception as e:
            return jsonify({"message": f"An error occurred: {e}"}), 500

    return render_template('register_customer.html')

@app.route('/register_employee', methods=['GET', 'POST'])
def register_employee():
    if request.method == 'POST':
        data = request.get_json()
        ename = data.get('ename')
        dob = data.get('dob')
        age = data.get('age')
        salary = data.get('salary')
        contact_number = data.get('contact_number')
        landline = data.get('landline')
        address = data.get('address')
        branch_id = data.get('branch_id')
        email = data.get('email')
        password = data.get('password')

        print("Data received from form: ", data)  # Debug statement

        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Insert new employee
            cursor.execute('''
                INSERT INTO Employee (Ename, DOB, Age, Salary, Contact_NO_1, Landline_No, Address, Email, Branch_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ename, dob, age, salary, contact_number, landline, address, email, branch_id))
            
            # Insert into Users table
            cursor.execute('INSERT INTO Users (Email, Password, Role) VALUES (?, ?, ?)', (email, password, 'employee'))
            
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Employee registered successfully"}), 200
        except sqlite3.IntegrityError as e:
            print("IntegrityError: ", e)  # Debug statement
            return jsonify({"message": "Email already exists"}), 400
        except Exception as e:
            print("Exception: ", e)  # Debug statement
            return jsonify({"message": f"An error occurred: {e}"}), 500

    return render_template('register_employee.html')

@app.route('/account_balance')
def account_balance():
    if 'user_id' in session and session['role'] == 'customer':
        user_id = session['user_id']
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Ensure Customer_ID is being used correctly
            cursor.execute('SELECT Balance FROM Account WHERE Customer_ID = ?', (user_id,))
            balance = cursor.fetchone()
            conn.close()

            if balance:
                return jsonify({"balance": balance[0]})
            else:
                return jsonify({"message": "No account found for this customer"}), 404
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": "Error fetching balance"}), 500
    return redirect(url_for('login'))

@app.route('/transfer_funds', methods=['POST'])
def transfer_funds():
    if 'user_id' in session and session['role'] == 'customer':
        data = request.get_json()
        to_email = data.get('to_email')
        amount = data.get('amount')
        
        if not to_email or not amount:
            return jsonify({"message": "Missing email or amount"}), 400
        
        user_id = session['user_id']
        
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Get the account number and balance of the sender
            cursor.execute('SELECT Account_No, Balance FROM Account WHERE Customer_ID = ?', (user_id,))
            sender_account = cursor.fetchone()
            
            if not sender_account:
                return jsonify({"message": "Sender account not found"}), 404
            
            sender_account_no, sender_balance = sender_account
            
            if sender_balance < amount:
                return jsonify({"message": "Insufficient funds"}), 400
            
            # Get the account number of the recipient
            cursor.execute('''
                SELECT Account_No FROM Account
                INNER JOIN Customer ON Account.Customer_ID = Customer.Customer_ID
                WHERE Customer.Email = ?
            ''', (to_email,))
            recipient_account = cursor.fetchone()
            
            if not recipient_account:
                return jsonify({"message": "Recipient account not found"}), 404
            
            recipient_account_no = recipient_account[0]
            
            # Perform the transfer
            new_sender_balance = sender_balance - amount
            cursor.execute('UPDATE Account SET Balance = ? WHERE Account_No = ?', (new_sender_balance, sender_account_no))
            
            cursor.execute('SELECT Balance FROM Account WHERE Account_No = ?', (recipient_account_no,))
            recipient_balance = cursor.fetchone()[0] + amount
            cursor.execute('UPDATE Account SET Balance = ? WHERE Account_No = ?', (recipient_balance, recipient_account_no))
            
            # Record the transaction
            cursor.execute('''
                INSERT INTO "Transaction" (Amount, Date, Sender_ID, Receiver_ID, Account_No)
                VALUES (?, ?, ?, ?, ?)
            ''', (amount, datetime.date.today(), user_id, recipient_account_no, sender_account_no))
            
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Transfer successful"})
        
        except Exception as e:
            print(f"Error during transfer: {e}")
            return jsonify({"message": "Error performing transfer"}), 500
    else:
        return jsonify({"message": "User not authenticated or not a customer"}), 403




@app.route('/add_money', methods=['POST'])
def add_money():
    if 'user_id' in session and session['role'] == 'customer':
        data = request.get_json()
        amount = data.get('amount')
        
        if amount is None or amount <= 0:
            return jsonify({"message": "Invalid amount"}), 400
        
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Retrieve the account number associated with the user
            cursor.execute('SELECT Account_No FROM Account WHERE Customer_ID = ?', (session['user_id'],))
            account = cursor.fetchone()
            if not account:
                return jsonify({"message": "No account found for this customer"}), 404
            
            account_no = account[0]
            
            # Update the balance
            cursor.execute('UPDATE Account SET Balance = Balance + ? WHERE Account_No = ?', (amount, account_no))
            
            # Record the transaction
            cursor.execute('INSERT INTO "Transaction" (Amount, Date, Sender_ID, Account_No) VALUES (?, ?, ?, ?)', 
                           (amount, datetime.date.today(), session['user_id'], account_no))
            
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Money added successfully"})
        except sqlite3.Error as e:
            conn.rollback()  # Rollback in case of error
            return jsonify({"message": f"An error occurred: {e}"}), 500
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    return redirect(url_for('login'))

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user_id' in session and session['role'] == 'customer':
        return render_template('customer_dashboard.html', first_name=session['first_name'])
    return redirect(url_for('login'))

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'employee_name' in session:
        return render_template('employee_dashboard.html', ename=session['employee_name'])
    else:
        return redirect(url_for('login'))  # Redirect to login if not logged in

@app.route('/view_transactions')
def view_transactions():
    if 'user_id' in session and session['role'] == 'employee':
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM "Transaction"
        ''')
        transactions = cursor.fetchall()
        conn.close()
        
        return render_template('transaction_history.html', transactions=transactions)
    return redirect(url_for('login'))


@app.route('/apply_for_loan', methods=['POST'])
def apply_for_loan():
    if 'user_id' in session and session['role'] == 'customer':
        data = request.get_json()
        amount = data.get('amount')
        purpose = data.get('purpose')
        
        if not amount or not purpose:
            return jsonify({"message": "Amount and Purpose are required"}), 400
        
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Print debug information
            print(f"Inserting Loan: Amount={amount}, Purpose={purpose}, UserID={session['user_id']}")
            
            # Insert loan application
            cursor.execute('''
                INSERT INTO Loan (Amount, Purpose, Issue_Date, Due_Date, Status, Customer_ID)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                amount,
                purpose,
                datetime.date.today(),
                datetime.date.today() + datetime.timedelta(days=30),
                'Pending',
                session['user_id']
            ))
            
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Loan application submitted successfully"}), 200
        except Exception as e:
            print(f"An error occurred during loan application: {e}")
            return jsonify({"message": f"An error occurred: {e}"}), 500
    else:
        return jsonify({"message": "User not authenticated or not a customer"}), 403


@app.route('/view_loans', methods=['GET'])
def view_loans():
    if 'user_id' in session and session['role'] == 'employee':
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()

            # Fetch loan data from the database with explicit table references
            cursor.execute('''
                SELECT 
                    Loan.Loan_ID, 
                    Loan.Amount, 
                    Loan.Purpose, 
                    Loan.Issue_date, 
                    Loan.Due_date, 
                    Loan.Status, 
                    Loan.Customer_ID, 
                    Customer.First_Name, 
                    Customer.Last_Name
                FROM Loan
                JOIN Customer ON Loan.Customer_ID = Customer.Customer_ID
            ''')

            loans = cursor.fetchall()
            conn.close()

            # Check the fetched data
            print(loans)  # Debugging line

            # Prepare data as list of dictionaries
            loans_data = []
            for loan in loans:
                loans_data.append({
                    'Loan_ID': loan[0],
                    'Amount': loan[1],
                    'Purpose': loan[2],
                    'Issue_date': loan[3],
                    'Due_date': loan[4],
                    'Status': loan[5],
                    'Customer_ID': loan[6],
                    'First_Name': loan[7],
                    'Last_Name': loan[8]
                })

            # Render the template with loan data
            return render_template('view_loans.html', loans=loans_data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"message": f"An error occurred: {e}"}), 500
    else:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

@app.route('/loan_status', methods=['GET'])
def loan_status():
    if 'user_id' in session and session['role'] == 'customer':
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()

            # Fetch loan data for the logged-in customer
            cursor.execute('''
                SELECT Loan_ID, Amount, Purpose, Issue_date, Due_date, Status
                FROM Loan
                WHERE Customer_ID = ?
            ''', (session['user_id'],))

            loans = cursor.fetchall()
            conn.close()

            # Prepare data as list of dictionaries
            loans_data = []
            for loan in loans:
                loans_data.append({
                    'Loan_ID': loan[0],
                    'Amount': loan[1],
                    'Purpose': loan[2],
                    'Issue_date': loan[3],
                    'Due_date': loan[4],
                    'Status': loan[5]
                })

            return jsonify(loans=loans_data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"message": f"An error occurred: {e}"}), 500
    else:
        return redirect(url_for('login'))



@app.route('/update_loan_status', methods=['POST'])
def update_loan_status():
    if 'user_id' in session and session['role'] == 'employee':
        data = request.get_json()
        loan_id = data.get('loan_id')
        status = data.get('status')
        
        if not loan_id or not status or status not in ['Granted', 'Rejected']:
            return jsonify({"message": "Invalid loan ID or status"}), 400
        
        try:
            conn = sqlite3.connect('bank.db')
            cursor = conn.cursor()
            
            # Update loan status
            cursor.execute('''
                UPDATE Loan
                SET Status = ?
                WHERE Loan_ID = ?
            ''', (status, loan_id))
            
            conn.commit()
            conn.close()
            
            return jsonify({"message": "Loan status updated successfully"}), 200
        except Exception as e:
            print(f"An error occurred during loan status update: {e}")
            return jsonify({"message": f"An error occurred: {e}"}), 500
    else:
        return jsonify({"message": "User not authenticated or not an employee"}), 403

def deduct_loan_amounts():
    try:
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        
        today = datetime.date.today()
        cursor.execute('''
            SELECT Loan_ID, Amount, Customer_ID
            FROM Loan
            WHERE Due_Date <= ? AND Status = 'Granted'
        ''', (today,))
        
        loans = cursor.fetchall()
        
        for loan in loans:
            loan_id, amount, customer_id = loan
            
            # Deduct amount + 100 from customer's account
            cursor.execute('''
                SELECT Balance
                FROM Customer
                WHERE Customer_ID = ?
            ''', (customer_id,))
            
            balance = cursor.fetchone()[0]
            new_balance = balance - (amount + 100)
            
            if new_balance < 0:
                new_balance = 0  # Handle overdraft or insufficient funds case
                
            cursor.execute('''
                UPDATE Customer
                SET Balance = ?
                WHERE Customer_ID = ?
            ''', (new_balance, customer_id))
            
            # Optionally, update loan status to 'Completed' or similar
            cursor.execute('''
                UPDATE Loan
                SET Status = 'Completed'
                WHERE Loan_ID = ?
            ''', (loan_id,))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred during loan deduction: {e}")

@app.route('/deduct_loans', methods=['GET'])
def deduct_loans():
    try:
        deduct_loan_amounts()
        return jsonify({"message": "Loan amounts deducted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    create_database()
    
    

    app.run(debug=True)
