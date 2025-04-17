from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret123'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="santosh227",  # Use your MySQL root password
    database="login_db"
)
cursor = db.cursor()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        dob = request.form['dob']
        email = request.form['email']
        address = request.form['address']
        password = generate_password_hash(request.form['password'])

        try:
            cursor.execute("""
                INSERT INTO users (name, age, dob, email, address, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, age, dob, email, address, password))
            db.commit()
            msg = "Registration Successful!"
        except:
            msg = "Email already exists!"
    return render_template('register.html', message=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[6], password):
            session['user'] = user[1]  # name
            return f"Welcome, {user[1]}!"
        else:
            msg = "Invalid email or password."
    return render_template('login.html', message=msg)

if __name__ == '__main__':
    app.run(debug=True)