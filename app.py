from flask import Flask, render_template, redirect, request, session, flash
import pymysql
from wtforms import Form, TextField, PasswordField, validators
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
DB_HOST      = "aws-project-362.cxt6a6u8d073.us-east-1.rds.amazonaws.com"
DB_USER      = "admin"
DB_PASS      = "group362"
DB_NAME      = "LIBRARY"

#Connecting to MySQL instance RDS
def db_connect():
    try:
        db = pymysql.connect(host=DB_HOST, port=3306, user=DB_USER, password=DB_PASS, db=DB_NAME)
        return db
    except Exception as e:
        print(str(e))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_msg =''
    # check if user has filled out all of the input
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        # grab input from request form
        username, password, email, firstname, lastname = request.form['username'], request.form['password'], request.form['email'], request.form['firstname'], request.form['lastname']
        # connect to mysql database
        db = db_connect()

        try:
            with db.cursor() as cur:
                # query the user account first
                cur.execute("SELECT * FROM PERSON WHERE username=%s", (username))
                user = cur.fetchone()

                # check if user account already exist
                if user:
                    error_msg = "Account already exist! Try another username"
                elif not re.match(r'[A-Za-z]+', firstname):
                    error_msg = "Invalid first name!"
                elif not re.match(r'[A-Za-z]+', lastname):
                    error_msg = "Invalid last name!"
                elif not re.match(r'[A-Za-z0-9_.-]+', username):
                    # username allow A-Z, a-z, 0-9, characters like _, ., -
                    error_msg = "Invalid username!"
                elif not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
                    # password need to have at least 8 character that matches
                    # A-Z, a-z, 0-9, characters like @, #, $, %, ^, &, +, =
                    error_msg = "Invalid password!"
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    # email needs a @ and also a . after @
                    error_msg = "Invalid email!"
                elif not firstname or not lastname or not username or not password or not email:
                    error_msg = "Field missing, please fill out everything!"
                else:
                    # create the user in the database
                    cur.execute("INSERT INTO PERSON VALUES (NULL, %s, %s, %s, %s, %s, %s)", (firstname, lastname, email, "user", username, password))
                    error_msg = "You have successfully registered!" # not an error msg
                    db.commit() # save registered account into database
        finally:
            db.close() # close mysql connection

    return render_template('register.html', error_msg = error_msg)

if __name__ == "__main__":
    app.run(debug=True)
