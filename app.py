from flask import Flask, render_template, request, session
from flask import Flask, render_template, request, session

import mysql.connector

app = Flask(__name__)
app.secret_key = 'a'

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="harshisonsql",
        database="cloud"
    )

def show_all(cursor):
    cursor.execute("SELECT * FROM user")
    for row in cursor.fetchall():
        print("The Name is :", row["name"])
        print("The E-mail is :", row["email"])
        print("The Contact is :", row["contact"])
        print("The Address is :", row["address"])
        print("The Role is :", row["role"])
        print("The Branch is :", row["branch"])
        print("The Password is :", row["password"])

def get_details(cursor, email, password):
    cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
    for row in cursor.fetchall():
        print("The Name is :", row["name"])
        print("The E-mail is :", row["email"])
        print("The Contact is :", row["contact"])
        print("The Address is :", row["address"])
        print("The Role is :", row["role"])
        print("The Branch is :", row["branch"])
        print("The Password is :", row["password"])

def insert_data(cursor, name, email, contact, address, role, branch, password):
    cursor.execute("INSERT INTO user (name, email, contact, address, role, branch, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, email, contact, address, role, branch, password))
    print("Number of affected rows:", cursor.rowcount)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login1')
def login1():
    return render_template('login.html')

@app.route('/portal')
def portal():
    return render_template('portal.html')

@app.route('/reges')
def reges():
    return render_template('registration.html')

@app.route('/up')
def up():
    return render_template('userprofile.html')

conn = get_connection()
print("Connection successful...")

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        contact = request.form['mobile']
        address = request.form['address']
        role = request.form['role']
        if role =="0":
            role = "Faculty"
        else:
            role = "Student"
        branch = request.form['branch']
        password = request.form['pwd']
        
        cursor = conn.cursor(dictionary=True)
        insert_data(cursor, name, email, contact, address, role, branch, password)
        conn.commit()
        cursor.close()
        return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pwd']
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        userdetails = cursor.fetchone()
        cursor.close()
        if userdetails:
            session['register'] = userdetails["email"]
            return render_template('userprofile.html', name=userdetails["name"], email=userdetails["email"], contact=userdetails["contact"], address=userdetails["address"], role=userdetails["role"], branch=userdetails["branch"])
        else:
            msg = "Incorrect Email id or Password"
            return render_template("login.html", msg=msg)
    return render_template('portal.html')

if __name__ == '__main__':
    app.run(debug=True)
