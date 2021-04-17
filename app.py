from flask import Flask, render_template, redirect, request, session, flash
import pymysql
from wtforms import Form, TextField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from functools import wraps
import config
# import boto3
import re
import gc
import sys
import logging
import os
# from flask_wtf.csrf import CsrfProtect

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
# CsrfProtect(app)
app.secret_key = 'hjkdjeuqoe157!@'


#customhost = <your db endpoint address>
DB_HOST      = "database-1.cykqbf99bmvw.us-west-1.rds.amazonaws.com"
# DB_HOST      = "database-1.cykqbf99bmvw.us-west-1.rds.amazonaws.com"
DB_USER      = "admin"
DB_PASS      = "group362"
#DB_PASS      = "adminadmin"
DB_NAME      = "LIBRARY"

#Path to save profile pictures
DIR_PATH = "/home/kient/project362/cpsc362-group-project/static/images"
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

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect('/login')
    return wrap

@app.route('/login', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        if request.method == 'POST':
            cursor = db.cursor()
            username = request.form['username']
            data = cursor.execute("SELECT * FROM PERSON WHERE Username = (%s)", (username))
            data = cursor.fetchone()
            cursor.close()

            if sha256_crypt.verify(request.form['password'], data[6]):
                session['logged_in']    = True
                session['username']     = username
                session['first_name']   = data[1]
                session['pic_name']     = data[7]
                flash("You are now logged in")
                return redirect('/dashboard')
            else:
                error = "Invalid credentials, try again."
        gc.collect()
        return render_template("login.html", error=error)

    except Exception as e:
        error = str(e)
        return render_template("login.html", error = error)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dahboard():
    username    = session['username']
    first_name  = session['first_name']
    ''' ***********************************************************************
    --- This will update the latest uploaded image to appear on the dashboad page,
    --- which occurs at @app.route('/change_pic') ---
    *************************************************************************'''
    cursor  = db.cursor()
    data    = cursor.execute("SELECT * FROM PERSON WHERE Username = (%s)", (username))
    data    = cursor.fetchone()
    session['pic_name'] = data[7]
    pic_name = session['pic_name']

    #Getting all the book information
    books    = cursor.execute("SELECT * FROM BOOK")
    books    = cursor.fetchall()
    cursor.close()

    gc.collect()
    return render_template('dashboard.html', first_name=first_name, pic_name=pic_name, books=books, counter=0)


@app.route('/dashboard/change_passwd', methods=['GET', 'POST'])
@login_required
def change_passwd():
    error = ''
    username = session['username']
    pic_name = session['pic_name']
    try:
        form = ChangePasswordForm(request.form)
        if request.method == 'POST' and form.validate():
            ''' ***************************************************************
            --- Extracting fields filled out by user in the change password form
            *****************************************************************'''
            oldpassword = form.old_password.data
            newpassword = form.new_password.data
            confirm     = form.confirm.data

            cursor  = db.cursor()
            data    = cursor.execute("SELECT * FROM PERSON WHERE Username = (%s)", (username))
            data    = cursor.fetchone()
            cursor.close()

            ''' ***************************************************************
            --- Validating if the new passwords are entered correctly
            ---     If it's not, then the program will display an error on the web
            ---     page and ask for another try.
            ---     If they are equal, then the program will compare the hash values
            ---     between the old_password (entered by user) and the current password
            ---     stored in the db. If they are not the same, an error will be
            ---     displayed and user will have another attempt. If they are
            ---     equal, then the program will update the new password to db.
            *****************************************************************'''
            if newpassword != confirm:
                error = "New password must match"
            else:
                if sha256_crypt.verify(oldpassword, data[6]):
                    new_password = sha256_crypt.encrypt((str(newpassword)))
                    # update the new password to the database
                    cursor = db.cursor()
                    data = cursor.execute("UPDATE PERSON SET Password = (%s) WHERE Username = (%s)", (new_password, username))
                    # data = cursor.fetchone()
                    db.commit()
                    cursor.close()
                    flash("You have changed your password!")
                    return redirect('/dashboard')
                else:
                    error = "Invalid old password, try again."
        else:
            error = "Please fill in all of the field in the form"

        gc.collect()
        return render_template('change_passwd.html', error=error, first_name=username, form=form, pic_name=pic_name)
    except Exception as e:
        error = str(e)

        return render_template('change_passwd.html', error=error, form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    gc.collect()
    flash("You have been logged out")
    return redirect('/')

@app.route('/dashboard/change_pic', methods=['GET', 'POST'])
@login_required
def change_pic():
    error = ''
    username   = session['username']
    first_name = session['first_name']
    pic_name   = session['pic_name']
    try:
        form = PhotoForm()
        if form.validate_on_submit():
            pic_name = form.new_photo.data
            filename = secure_filename(pic_name.filename)
            ''' ****************************************************************
            ---------- Save the newly updated picture locally ----------
            *****************************************************************'''
            pic_name.save(os.path.join(DIR_PATH, pic_name.filename))

            ''' ****************************************************************
            ---------- Update Profile_URL (filename of pix) to db ----------
            ******************************************************************'''
            cursor  = db.cursor()
            data    = cursor.execute("UPDATE PERSON SET Profile_URL = (%s) WHERE Username = (%s)",
                                    (pic_name.filename, username))
            db.commit()
            cursor.close()
            gc.collect()
            flash("You have successfully updated your profile picture")
            return redirect('/dashboard')
        # gc.collect()
        app.logger.info('Yes14~~')
        return render_template('change_pic.html', pic_name=pic_name, first_name=first_name, error=error, form=form)
    except Exception as e:
        error = str(e)
        return render_template('change_pic.html', pic_name=pic_name, first_name=first_name, error=error, form=form)

@app.route('/dashboard/books/<string:isbn>', methods=['GET', 'POST'])
@login_required
def view_and_comment_book(isbn):
    # =========get book info=========
    cursor  = db.cursor()
    data    = cursor.execute("SELECT * FROM BOOK WHERE ISBN = (%s)", (isbn))
    data    = cursor.fetchone()
    cursor.close()

    # =========post user comment=========
    if request.method == 'POST' and 'comment' in request.form:
        username = session['username']
        comment = request.form['comment']

        # get current user id by username
        cursor = db.cursor()
        uid = cursor.execute("SELECT id FROM PERSON WHERE Username = (%s)", (username))
        uid = int(cursor.fetchone()[0])
        cursor.close()

        # commit data to comment database
        cursor = db.cursor()
        cursor.execute("INSERT INTO COMMENT(DatePosted, Comment, Rating, PersonID, ISBN) VALUES (NOW(), %s, 5, %s, %s)", (comment, uid, isbn))
        db.commit()
        cursor.close()
        gc.collect()

    # =========get user comment=========
    cursor   = db.cursor()
    comments = cursor.execute("SELECT * FROM COMMENT WHERE ISBN = (%s)", (isbn))
    comments = cursor.fetchall()
    cursor.close()

    users = []
    cursor   = db.cursor()
    for comment in comments:
        user = cursor.execute("SELECT Username FROM PERSON WHERE id = (%s)", (comment[4]))
        user = cursor.fetchone()
        users.append(user[0])
    cursor.close()

    return render_template('/view_book.html', data=data, comments=comments, users=users, isbn=isbn, counter=0)

if __name__ == "__main__":
    app.run(debug=True)
