# Online Bank Database Management System

## Overview
The Online Bank Database Management System is a comprehensive web application designed to streamline essential banking operations for both customers and employees. Developed using **HTML**, **CSS**, **JavaScript**, **Flask**, and **MySQL**, this project integrates user-friendly interfaces with robust backend logic and database management.

## Features

### Customer Portal:
- **Secure Login**: Customers can log in securely to access their account.
- **Fund Transfer**: Transfer funds seamlessly to other registered customers within the system.
- **Loan Application**: Submit loan requests directly through the portal.
- **Balance Check**: View real-time account balances and transaction details.

### Employee Portal:
- **Secure Login**: Separate login for employees to access administrative functionalities.
- **Loan Management**: Approve or reject customer loan applications based on eligibility and criteria.
- **Customer Management**: Access and review detailed information and statistics of all registered customers.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python Framework)
- **Database**: MySQL

## Installation and Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Yashwanth0530/online-bank-database-system.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd online-bank-database-system
   ```

3. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up the Database**:
   - Install MySQL and create a database named `bank_db`.
   - Import the provided SQL schema file:
     ```sql
     mysql -u username -p bank_db < schema.sql
     ```
   - Update the database configuration in the `config.py` file.

6. **Run the Application**:
   ```bash
   flask run
   ```
   Access the app at `http://127.0.0.1:5000/`.

## Directory Structure
```
|-- static/
|   |-- images/
|   |-- styles/
|-- templates/
|   |-- index.html
|   |-- register_customer.html
|   |-- register_employee.html
|   |-- list_customers.html
|   |-- transaction_history.html
|   |-- view_loans.html
|   |-- customer_dashboard.html
|   |-- employee_dashboard.html

|-- app.py

|-- README.md
|-- requirements.txt
```

## Future Enhancements
- **Enhanced Security**: Implement two-factor authentication for added security.
- **Reporting Tools**: Add analytics and reporting tools for employees.
- **Mobile Responsiveness**: Optimize the application for mobile devices.
- **Transaction History**: Allow customers to view detailed transaction histories.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For queries or contributions, contact [P Yashwanth Kumar] at [yashwanthp530@gmail.com].
