import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from random import randint
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret' # Make sure to change this to your own value!!!

def db_connect():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    return "Welcome to SMS OTP server! You can generate an OTP at GET /create or verify at POST /verify! This is the backend server with no frontend :)"

@app.route("/create", methods=("GET","POST"))
def create():
    if request.method == "POST":
        conn = db_connect()

        # Create OTP
        otp = randint(100000, 999999)
        expiry = datetime.strftime((datetime.now(tz=None) + timedelta(minutes=1)), '%Y-%m-%d %H:%M:%S')
        # Insert into DB
        insert = conn.execute('INSERT INTO otps (otp, expiry) VALUES (?, ?)', (otp, expiry))
        conn.commit()
        conn.close()
    
        return str(otp)

    return "This is the API to create a new 6-digit OTP! Just send a post request with no form data and you will be returned a 6-digit OTP!"

@app.route("/verify", methods=("GET","POST"))
def verify():
    if request.method == "POST":  
        print(request.host)
        conn = db_connect() 
        otp = request.form['otp']
        f = '%Y-%m-%d %H:%M:%S'
        try:
            expiry = conn.execute('SELECT expiry FROM otps WHERE otp = ?', (otp,)).fetchone()[0]
        except:
            return("OTP invalid")
        if (datetime.strptime(expiry,f) - datetime.now()).seconds / 60 > 1:
            conn.execute('DELETE from otps where otp = ?', (otp,))
            conn.commit()
            conn.close()
            return("OTP expired")
        else:
            return("OTP verified")
    return "This is the API to verify your 6-digit OTP! Just send a post request with no form-data {otp: <your otp>} and you will know if the OTP is valid, invalid or expired."