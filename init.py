from flask import Flask, render_template, redirect, request, session, flash, url_for
import pymysql
from wtforms import Form, TextField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from functools import wraps
from time import gmtime, strftime
import config
import re
import gc
import sys
import logging
import os

#Registration form that can validate user inputs
#To use validators.Email, first install $ pip3 install wtforms[email]
class RegistrationForm(Form):
    fname    = TextField('First name', [validators.Length(min=1, max=30)])
    lname    = TextField('Last name', [validators.Length(min=1, max=30)])
    email    = EmailField('Email address', [validators.Length(min=6, max=50),
                                            validators.Email(message="Enter a valid email"),
                                            validators.DataRequired()])
    username = TextField('Username', [validators.Length(min=4, max=100)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6, max=20),
                                          validators.EqualTo('confirm', message="Password must match")])
    confirm  = PasswordField('Repeat Password')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', [validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.DataRequired(), validators.Length(min=6, max=20),
                                          validators.EqualTo('confirm', message="Password must match")])
    confirm  = PasswordField('Repeat New Password')

class PhotoForm(FlaskForm):
    new_photo = FileField('Upload a new picture', validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')
