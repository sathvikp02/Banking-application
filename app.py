# Import necessary libraries
from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response # type: ignore
import pyodbc # type: ignore
import hashlib
import os
from werkzeug.utils import secure_filename # type: ignore

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

conn_str = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=upfdb.database.windows.net,1433;'
    'DATABASE=upfdb;'
    'UID=bindu;'
    'PWD=Password123;'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

# Establish a database connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# account_name = "upfbankstorage"
# container_name = "upfblob"

# blob_service_client = BlobServiceClient(f"https://upfblob.blob.core.windows.net", account_key)

# Create a table if it doesn't exist
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        username NVARCHAR(50) NOT NULL,
        password NVARCHAR(256) NOT NULL,
        balance FLOAT DEFAULT 0.0,
        kyc_filename NVARCHAR(255),
        loan_amount FLOAT DEFAULT 0.0
    )
''')
conn.commit()

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'transactions')
    CREATE TABLE transactions (
        id INT PRIMARY KEY IDENTITY(1,1),
        username NVARCHAR(50) NOT NULL,
        transaction_date DATETIME DEFAULT GETDATE(),
        transaction_type NVARCHAR(50) NOT NULL,
        amount FLOAT NOT NULL
    )
''')
conn.commit()


# Dummy user for demonstration purposes
def insert_dummy_users():
    dummy_users = [
        ('user1', 'password1'),
        ('user2', 'password2'),
        ('user3', 'password3'),
        ('user4', 'password4'),
        ('user5', 'password5'),
    ]

    for username, password in dummy_users:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, 0.0)',
                       username, hashed_password)
        conn.commit()

# Uncomment the line below if you want to insert dummy users
# insert_dummy_users()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', username, hashed_password)
        user = cursor.fetchone()

        if user:
            session['username'] = username

            if user.balance == 0.0:
                cursor.execute('UPDATE users SET balance = 20000.0 WHERE id = ?', user.id)
                conn.commit()

            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')  # Flash an error message
            return render_template('login.html')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('SELECT * FROM users WHERE username = ?', username)
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('signup.html', error='Username already exists')

        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                       username, hashed_password)
        conn.commit()

        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('signup.html', error=None)


# Function to apply for a loan
@app.route('/apply_loan', methods=['GET', 'POST'])
def apply_loan():
    if 'username' in session:
        if request.method == 'POST':
            try:
                # Extract loan amount from the form data
                loan_amount = float(request.form.get('loan_amount', 0))

                # Check if the loan amount is positive
                if loan_amount <= 0:
                    flash('Loan amount must be greater than 0.', 'danger')
                    return redirect(url_for('dashboard'))

                # Update the user's loan amount in the 'users' table
                cursor.execute('''
                        UPDATE users
                        SET loan_amount = loan_amount + ?
                        WHERE username = ?;
                    ''', loan_amount, session['username'])
                conn.commit()

                # Flash message for successful loan application
                flash(f'Loan of Rs {loan_amount} applied successfully!', 'success')

                # Redirect to the dashboard
                return redirect(url_for('apply_loan'))

            except Exception as e:
                # Flash message for any error during loan application
                flash(f'Error applying for a loan: {str(e)}', 'danger')
                return redirect(url_for('dashboard'))

        else:
            return render_template('apply_loan.html')  # Render the apply_loan.html template for GET requests

    return redirect(url_for('login'))


# Route for account balance
@app.route('/account_balance')
def account_balance():
    if 'username' in session:
        cursor.execute('SELECT balance, loan_amount FROM users WHERE username = ?', session['username'])
        user_info = cursor.fetchone()

        balance = user_info.balance
        loan_amount = user_info.loan_amount

        # Calculate the total account balance including the loan amount
        total_balance = balance + loan_amount  # Use '+' instead of '-'

        return render_template('account_balance.html', username=session['username'], total_balance=total_balance)

    else:
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        cursor.execute('SELECT * FROM users WHERE username = ?', session['username'])
        user = cursor.fetchone()

        return render_template('dashboard.html', username=session['username'], balance=user.balance)
    else:
        return redirect(url_for('login'))


# Route for fund transfer
@app.route('/fund_transfer', methods=['GET', 'POST'])
def fund_transfer():
    if 'username' in session:
        if request.method == 'POST':
            try:
                beneficiary_username = request.form.get('beneficiary_username')
                transfer_amount = float(request.form.get('transfer_amount'))

                cursor.execute('SELECT * FROM users WHERE username = ?', beneficiary_username)
                beneficiary = cursor.fetchone()

                if beneficiary:
                    cursor.execute('UPDATE users SET balance = balance - ? WHERE username = ?', transfer_amount,
                                   session['username'])

                    cursor.execute('UPDATE users SET balance = balance + ? WHERE username = ?', transfer_amount,
                                   beneficiary_username)

                    cursor.execute('INSERT INTO transactions (username, transaction_type, amount) VALUES (?, ?, ?)',
                                   (session['username'], 'Transfer (To: {})'.format(beneficiary_username), transfer_amount))

                    cursor.execute('INSERT INTO transactions (username, transaction_type, amount) VALUES (?, ?, ?)',
                                   (beneficiary_username, 'Transfer (From: {})'.format(session['username']),
                                    transfer_amount))

                    conn.commit()

                    # Flash message for successful fund transfer
                    flash(f'Funds transferred successfully to {beneficiary_username}!', 'success')

                    return redirect(url_for('fund_transfer'))
                else:
                    return render_template('fund_transfer.html', username=session['username'],
                                           error='Beneficiary not found')

            except Exception as e:
                # Flash message for any error during fund transfer
                flash(f'Error transferring funds: {str(e)}', 'danger')
                return render_template('fund_transfer.html', username=session['username'], error=str(e))

        return render_template('fund_transfer.html', username=session['username'], error=None)
    else:
        return redirect(url_for('login'))


@app.route('/transaction_history')
def transaction_history():
    if 'username' in session:
        cursor.execute('SELECT * FROM transactions WHERE username = ? ORDER BY transaction_date DESC', session['username'])
        transaction_history = cursor.fetchall()
        return render_template('transaction_history.html', username=session['username'],
                               transaction_history=transaction_history)
    else:
        return redirect(url_for('login'))




# Function to upload a file to Azure Blob Storage
# def upload_to_azure(file, filename):
#     blob_service_client = BlobServiceClient(f"https://upfblob.blob.core.windows.net", account_key)
#     container_client = blob_service_client.get_container_client(container_name)
#     blob_client = container_client.get_blob_client(filename)
#     blob_client.upload_blob(file)

# Function to store the association between the user and the uploaded KYC file in the database
# def store_kyc_association(username, filename):
#     cursor.execute('UPDATE users SET kyc_filename = ? WHERE username = ?', filename, username)
#     conn.commit()

# Route to handle KYC form submission
# @app.route('/upload_kyc_form', methods=['GET'])
# def upload_kyc_form():
#     if 'username' in session:
#         return render_template('upload_kyc_form.html', username=session['username'])
#     else:
#         return redirect(url_for('login'))

# @app.route('/download_kyc/<filename>')
# def download_kyc(filename):
#     if 'username' in session:
#         container_client = blob_service_client.get_container_client(container_name)
#         blob_client = container_client.get_blob_client(filename)

#         try:
#             blob_data = blob_client.download_blob().readall()
#             response = make_response(blob_data)
#             response.headers['Content-Type'] = 'application/octet-stream'
#             response.headers['Content-Disposition'] = f'attachment; filename={filename}'
#             return response
#         except Exception as e:
#             flash(f'Error downloading KYC form: {str(e)}', 'error')

#     return redirect(url_for('dashboard'))

@app.route('/sign_out', methods=['POST'])
def sign_out():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8008)
