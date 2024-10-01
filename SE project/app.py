from flask import Flask, render_template, request, redirect, url_for,jsonify,session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.static_folder = 'static'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Goog@0004'
app.config['MYSQL_DB'] = 'billing'

mysql = MySQL(app)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        data = request.json
        print("Received data:", data)  # Print received data to the console for verification
        items = data['items']
        username = session.get('username')  # Retrieve username from session

        # Check if the username exists in the orders table
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM orders WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if not existing_user:
            # Insert the username into the orders table if it doesn't exist
            cur.execute("INSERT INTO orders (username) VALUES (%s)", (username,))
            mysql.connection.commit()

        # Update the quantities of items in the cart
        for item, quantity in items.items():
            item_name = item.replace(' ', '_')
            query = f"UPDATE orders SET `{item_name}` =  %s WHERE username = %s"
            print("SQL query:", query)
            cur.execute(query, (quantity, username))
            try:
                mysql.connection.commit()
            except Exception as e:
                mysql.connection.rollback()
                print("Error committing transaction:", e)
            print(f"Updated quantity for item {item} to {quantity} for user {username}")  # Print successful update


        cur.close()
        return 'Items added to cart successfully'



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/maincourse.html')
def main_course():
    return render_template('maincourse.html')

@app.route('/beverages.html')
def beverages():
    return render_template('beverages.html')

@app.route('/starters.html')
def starters():
    return render_template('starters.html')

@app.route('/desserts.html')
def desserts():
    return render_template('desserts.html')

@app.route('/payment.html')
def payment():
    return render_template('payment.html')

@app.route('/thankyou.html')
def thankyou():
    return render_template('thankyou.html')






@app.route('/menu', methods=['POST'])
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
            if user_type == 'customer':
                return redirect(url_for('show_menu'))
            elif user_type == 'manager':
                return redirect(url_for('manager'))
            elif user_type == 'chef':
                return redirect(url_for('chef'))
            else:
                return 'Invalid user type'
        else:
            return 'Invalid username or password'

@app.route('/manager.html')
def manager():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch usernames ending with "@customer" from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM accounts WHERE username LIKE '%@customer'")
    usernames = [row[0] for row in cur.fetchall()]
    cur.close()

    return render_template('manager.html', usernames=usernames)


@app.route('/chef.html')
def chef():
    if 'username' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT o.username, o.* FROM orders o INNER JOIN accounts a ON o.username = a.username WHERE a.username LIKE %s", ('%@customer',))
    orders = cur.fetchall()

    if not orders:
        return "No items in the orders"

    items = []
    
    # Get column names from the cursor description
    column_names = [column[0] for column in cur.description]

    # Iterate over the orders
    for order in orders:
        username = order[0]
        order_data = order[1:]
        user_items = []
        # Iterate over the columns of the order
        for column_index, value in enumerate(order_data):
            # Skip the first column which is the 'username'
            if column_index == 0:
                continue
            # Get the column name without underscores
            if column_index < len(column_names):
                column_name_with_underscore = column_names[column_index]
                column_name = column_name_with_underscore.replace('_', ' ')
                # Check if the value is greater than 0
                if value > 0:
                    # Append item to the user_items list with two values: (column_name_with_underscore, value)
                    user_items.append((column_name_with_underscore, value))
        # Append the username and its items to the items list
        items.append((username, user_items))

    cur.close()

    return render_template('chef.html', items=items)



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




@app.route('/billing.html')
def billing():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE username = %s", (username,))
    order = cur.fetchone()

    print("Order:", order)  # Add this line to print out the order data

    if not order:
        return "No items in the order"

    items = []
    total = 0
    
    # Get column names from the cursor description
    column_names = [column[0] for column in cur.description]

    # Iterate over the columns of the order
    for column_index, value in enumerate(order):
        # Skip the first column which is the 'username'
        if column_index == 0:
            continue
        # Get the column name without underscores
        if column_index < len(column_names):
            column_name_with_underscore = column_names[column_index]
            column_name = column_name_with_underscore.replace('_', ' ')
            # Check if the value is greater than 0
            if value > 0:
                # Fetch the price from the prices table using the original item name
                cur.execute("SELECT price FROM prices WHERE item = %s", (column_name_with_underscore,))
                price_row = cur.fetchone()
                if price_row:
                    price = price_row[0]
                    print(f"Price for {column_name_with_underscore}: {price}")  # Debug print statement
                    total += value * price
                    # Append item to the items list with three values: (column_name_with_underscore, value, price)
                    items.append((column_name_with_underscore, value, price))
                else:
                    print(f"No price found for {column_name_with_underscore}")  # Debug print statement

    cur.close()

    return render_template('billing.html', items=items, total=total)




if __name__ == '__main__':
    app.run(debug=True)
