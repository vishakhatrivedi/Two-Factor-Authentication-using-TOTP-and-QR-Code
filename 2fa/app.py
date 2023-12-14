from flask import Flask, request, render_template, redirect, url_for, session
import pyotp
import pyqrcode
import os
import mysql.connector
import datetime

MAX_ATTEMPTS = 3
TOTP_INTERVAL = 30

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "userdata",
}

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'
app.config['STATIC_FOLDER'] = 'static'  # Name of your static folder
app.config['STATIC_URL_PATH'] = '/static'  # The URL path for static files


def generate_totp_key():
    key = pyotp.random_base32()
    return key

def generate_totp_uri(key, issuer="YourApp"):
    totp = pyotp.TOTP(key, interval=TOTP_INTERVAL)
    totp_uri = totp.provisioning_uri(issuer_name=issuer)
    return totp_uri

def create_user(connection, cursor, user_data):
    insert_query = """
        INSERT INTO logindata (id, username, password, position, department, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_query, user_data)
        connection.commit()
        print("User created successfully!")
    except mysql.connector.Error as err:
        print("Error: Failed to create user -", err)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def login(connection, cursor, login_data):
    select_query = """
        SELECT id, username, position, department FROM logindata WHERE username = %s AND password = %s
    """
    
    try:
        cursor.execute(select_query, login_data)
        result = cursor.fetchone()
        for _ in cursor:  # Iterate through all rows to fetch them
            pass

        cursor.close()  # Close the cursor after fetching all results
        return result is not None, result
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        raise

def insert_audit_log(connection, cursor, id, username, position, department, login_time, logout_time=None):
    insert_query = """
        INSERT INTO audit_logs (id,username, position, department, login_time, logout_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_query, (id, username, position, department, login_time, logout_time))
        connection.commit()
        print("Audit log inserted successfully!")
    except mysql.connector.Error as err:
        print("Error: Failed to insert audit log -", err)
        connection.rollback()
    finally:
        cursor.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        data = request.form
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            login_success, user_data = login(connection, cursor, (data['username'], data['password']))

            if login_success:
                key = generate_totp_key()

                session['totp_key'] = key
                session['attempts'] = MAX_ATTEMPTS

                if user_data:
                    id, username, position, department = user_data
                    session['id'] = id
                    session['username'] = username
                    session['position'] = position
                    session['department'] = department

                # Record login time
                login_time = datetime.datetime.now()
                session['login_time'] = login_time

                cursor.close()  # Close the cursor after fetching user data
                connection.commit()  # Commit changes to the database

                return redirect(url_for('verify'))
            else:
                response = {"message": "Login failed. Invalid credentials."}
                return render_template('login.html', message=response)
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            response = {"message": "Failed to log in. MySQL Error: " + str(err)}
            return render_template('login.html', message=response)
        except Exception as e:
            print("Error:", e)
            response = {"message": "Failed to log in. Error: " + str(e)}
            return render_template('login.html', message=response)
        finally:
            cursor.close()  # Ensure the cursor is always closed
            connection.close()  # Close the connection

    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'totp_key' in session and 'attempts' in session:
        key = session['totp_key']
        totp = pyotp.TOTP(key, interval=TOTP_INTERVAL)
        attempts = session['attempts']
        qr_image = None

        if request.method == 'POST':
            user_code = request.form.get('verification_code')
            if attempts > 0:
                if totp.verify(user_code):
                    session.pop('totp_key', None)
                    session.pop('attempts', None)
                    return render_template('verification_successful.html')
                else:
                    attempts -= 1
                    session['attempts'] = attempts
            if attempts == 0:
                return render_template('verification_attempts_exceeded.html')

        totp_uri = generate_totp_uri(key)
        qr = pyqrcode.create(totp_uri)
        qr_image = qr.png_as_base64_str(scale=6)

        return render_template('verify.html', qr_image=qr_image, attempts_remaining=attempts)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'login_time' in session:
        login_time = session['login_time']
        logout_time = datetime.datetime.now()
        id = session.get('id')
        username = session.get('username')
        position = session.get('position')
        department = session.get('department')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            insert_audit_log(connection, cursor, id, username, position, department, login_time, logout_time)
        except Exception as e:
            print("Error:", e)

        cursor.close()
        connection.close()

    session.pop('totp_key', None)
    session.pop('attempts', None)
    session.pop('login_time', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        data = request.form
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            create_user(connection, cursor, (
                data['id'],
                data['username'],
                data['password'],
                data['position'],
                data['department'],
                data['phone']
            ))
            response=("User created successfully!!")
            return render_template('register.html',message=response)
        except Exception as e:
            print("Error:", e)
            response = {"message": "Failed to create user.", "error": str(e)}
            return render_template('register.html', message=response)
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
