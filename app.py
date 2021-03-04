from flask import Flask, render_template, redirect, request, session, flash
import pymysql
from wtforms import Form, TextField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt
from functools import wraps
import config
# import boto3
import re
import gc
import sys
import logging
import os

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.secret_key = 'hjkdjeuqoe157!@'

#customhost = <your db endpoint address>
DB_HOST      = "cpsc362.cqz5lsbthplh.us-east-2.rds.amazonaws.com"
#DB_HOST      = "aws-project-362.cxt6a6u8d073.us-east-1.rds.amazonaws.com"
DB_USER      = "admin"
#DB_PASS      = "group362"
DB_PASS      = "adminadmin"
DB_NAME      = "LIBRARY"

#Connecting to MySQL instance RDS
try:
    db = pymysql.connect(host=DB_HOST, port=3306, user=DB_USER, password=DB_PASS, db=DB_NAME)
except Exception as e:
    print(str(e))

#Registration form that can validate user inputs
#To use validators.Email, first install $ pip3 install wtforms[email]
class RegistrationForm(Form):
    fname    = TextField('First name', [validators.Length(min=1, max=30)])
    lname    = TextField('Last name', [validators.Length(min=1, max=30)])
    email    = EmailField('Email address', [validators.Length(min=6, max=50),
                                            validators.Email(message="Enter a valid email"),
                                            validators.DataRequired()])
    username = TextField('Username', [validators.Length(min=4, max=100)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message="Password must match")])
    confirm  = PasswordField('Repeat Password')

@app.route('/')
def home():
    app.logger.info('Yes1~~')
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            first_name  = form.fname.data
            last_name   = form.lname.data
            email       = form.email.data
            usr_name    = form.username.data
            passwd      = sha256_crypt.encrypt((str(form.password.data)))
            role        = "user"

            #Checking for duplicate username
            cursor = db.cursor()
            x = cursor.execute("SELECT * FROM PERSON WHERE Username=(%s)", (usr_name))
            cursor.close()
            if int(x) > 0:
                flash("That username is already taken. Please choose another")
                return render_template('register.html', form=form)
            else:
                cursor = db.cursor()
                cursor.execute("INSERT INTO PERSON (Username, Password, Email, FirstName, LastName, Role) VALUES (%s, %s, %s, %s, %s, %s)",
                                (usr_name, passwd, email, first_name, last_name, role))
                db.commit()
                cursor.close()
                gc.collect()
                flash("You have successfully registered your account")
                return redirect('/')
        return render_template('register.html', form=form)
    except Exception as e:
        return(str(e))

@app.route('/login', methods=["GET","POST"])
def login_page():
    error = ''
    # app.logger.info('Yes7~~')
    try:
        if request.method == 'POST':
            # app.logger.info('Yes6~~')
            cursor = db.cursor()
            username = request.form['username']
            data = cursor.execute("SELECT * FROM PERSON WHERE Username = (%s)", (username))
            data = cursor.fetchone()
            cursor.close()

            if sha256_crypt.verify(request.form['password'], data[6]):
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = data[0]
                flash("You are now logged in")
                return redirect('/')
            else:
                error = "Invalid credentials, try again."
        gc.collect()
        # app.logger.info('Yes8~~')
        return render_template("login.html", error=error)

    except Exception as e:
        error = str(e)
        return render_template("login.html", error = error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dahboard():
    return Hello

if __name__ == "__main__":
    app.run(debug=True)
