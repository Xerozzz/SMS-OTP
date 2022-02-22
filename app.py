import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from random import randint
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret' 

def db_connect():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=("GET","POST"))
def index():
    return render_template("index.html")

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

        return render_template('create.html', otp=otp)

    return render_template("create.html")

@app.route("/verify", methods=("GET","POST"))
def verify():
    if request.method == "POST":  
        conn = db_connect() 
        otp = request.form['otp']
        f = '%Y-%m-%d %H:%M:%S'
        try:
            expiry = conn.execute('SELECT expiry FROM otps WHERE otp = ?', (otp,)).fetchone()[0]
        except:
            flash("OTP invalid")
            return redirect(url_for('verify'))
        if (datetime.strptime(expiry,f) - datetime.now()).seconds / 60 > 1:
            flash("OTP expired")
            conn.execute('DELETE from otps where otp = ?', (otp,))
            conn.commit()
            conn.close()
        else:
            flash("OTP verified")
        return redirect(url_for('verify'))
    return render_template("verify.html")