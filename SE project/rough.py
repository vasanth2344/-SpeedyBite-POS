from flask import Flask, render_template, request, redirect, url_for,jsonify,session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.static_folder = 'static'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sikeniggar'
app.config['MYSQL_DB'] = 'LMS'

mysql = MySQL(app)



@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login')
def login():
    return render_template('login.html')













@app.route('/home', methods=['POST'])
def menu():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the database to verify the credentials
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['username'] = username
            # Extract user type from the username
            user_type = username.split('@')[-1]
            if user_type == 'student':
                return redirect(url_for('home'))
            elif user_type == 'teacher':
                return redirect(url_for('teacher'))
            else:
                return 'Invalid user type'
        else:
            return 'Invalid username or password'



@app.route('/menu.html')
def show_menu():
    return render_template('menu.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone_number = request.form['phone_number']
        gmail = request.form['gmail']
        
        # Check if the username already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        cur.close()
        
        if existing_user:
            return render_template('signup.html', error='Account already exists')
        else:
            # Insert the new user into the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO accounts (username, password, name, phone_number, gmail) VALUES (%s, %s, %s, %s, %s)", 
                        (username, password, name, phone_number, gmail))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))  # Redirect to login page after successful signup
    else:
        return render_template('signup.html')


@app.route('/forgot')
def forgot_password():
    return render_template('forgot.html')

@app.route('/recover_password', methods=['POST'])
def recover_password():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']

        # Query the database to verify the user's information
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM accounts WHERE username = %s AND name = %s AND phone_number = %s AND gmail = %s", 
                    (username, name, phone_number, email))
        user = cur.fetchone()
        cur.close()

        if user:
            # Display the recovered password
            return f"Your password is: {user[0]}"
        else:
            return 'User information does not match. Please try again or contact support.'






if __name__ == '__main__':
    app.run(debug=True)
