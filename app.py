from flask import Flask, render_template, redirect, request, session, flash
import pymysql
from wtforms import Form, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import config
# import boto3
import gc
import sys
import logging
import os

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.secret_key = 'hjkdjeuqoe157!@'

#Connecting to MySQL instance RDS
try:
    db = pymysql.connect(host     = customhost,
                         port     = 3306,
                         user     = customuser,
                         password = custompass,
                         db       = customdb
                        )
except Exception as e:
    print(str(e))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

if __name__ == "__main__":
    app.run(debug=True)
