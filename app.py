from init import *
from config import *

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
# CsrfProtect(app)
app.secret_key = 'hjkdjeuqoe157!@'

#Path to save profile pictures
DIR_PATH = "static/images/users"
#Connecting to MySQL instance RDS
try:
    db = pymysql.connect(host=DB_HOST, port=3306, user=DB_USER, password=DB_PASS, db=DB_NAME)
except Exception as e:
    print(str(e))

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
    return render_template('dashboard.html', first_name=first_name, pic_name=pic_name, books=books)


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
            pic_name.save(os.path.join(os.path.abspath(DIR_PATH), pic_name.filename))

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
    cursor  = db.cursor()
    data    = cursor.execute("SELECT * FROM BOOK WHERE ISBN = (%s)", (isbn))
    data    = cursor.fetchone()
    cursor.close()
    username = session['username']

    if request.method == 'POST' and len(request.form['comment']) > 0:
        comment = request.form['comment']
        username = session['username']
        rating = 0;
        if 'rating' in request.form:
            rating = int(request.form['rating'])

        #Add and commit the comment and rating to the db
        cursor = db.cursor()
        cursor.execute("INSERT INTO COMMENT (DatePosted, Comment, Username, ISBN) VALUES (NOW(), %s, %s, %s)", (comment, username, isbn))
        rating_check = cursor.execute("SELECT * FROM RATING WHERE Username = (%s) AND ISBN = (%s)", (username, isbn))
        if rating_check == 0:
            cursor.execute("INSERT INTO RATING (Rating, Username, ISBN) VALUES (%s, %s, %s)", (rating, username, isbn))
            db.commit()
        #If the user wants to rate the same book again, executes this statement
        elif rating != 0:
            rating_check = cursor.fetchone()
            if int(rating_check[0]) != rating:
                cursor.execute("UPDATE RATING SET Rating = (%s) WHERE Username = (%s)", (rating, username))
                db.commit()
        #Calculate the average rating using ratings from all comments (with a currently viewed book)
        avg_rating = cursor.execute("SELECT AVG(Rating) FROM RATING WHERE ISBN = (%s)", (isbn))

        #When there's at least one rating returned by the query
        if avg_rating > 0:
            avg_rating = cursor.fetchone()
            cursor.execute("UPDATE BOOK SET AverageRating = (%s) WHERE ISBN = (%s)", (avg_rating[0], isbn))
            db.commit()
        cursor.close()
        gc.collect()
        return redirect(url_for('view_and_comment_book', isbn=isbn))
    else:
        #Query and output all comments to the page
        cursor = db.cursor()
        comment = cursor.execute("SELECT * FROM COMMENT WHERE ISBN = (%s)", (isbn))
        comment = cursor.fetchall()
        rating = cursor.execute("SELECT * FROM RATING WHERE ISBN = (%s)", (isbn))
        rating = cursor.fetchall()
        cursor.close()
        gc.collect()
        #Can globally access each isbn => simplicity and save time
        session['isbn'] = isbn
        return render_template('/view_book.html', data=data, rating=rating, comment=comment, username=username)

@app.route('/dashboard/delete/<string:commentID>', methods=['GET', 'POST'])
@login_required
def delete_comment(commentID):
    cursor = db.cursor()
    cursor.execute("DELETE FROM COMMENT WHERE CommentID = (%s)", (commentID))
    db.commit()
    cursor.close()
    gc.collect()
    isbn = session['isbn']
    return redirect(url_for('view_and_comment_book', isbn=isbn))

@app.route('/dashboard/edit/<string:commentID>', methods=['GET', 'POST'])
@login_required
def edit_comment(commentID):
    error = ''
    cursor = db.cursor()
    comment = cursor.execute("SELECT * FROM COMMENT WHERE CommentID = (%s)", commentID)
    comment = cursor.fetchone()
    cursor.close()
    gc.collect()

    comment_user = comment[3]

    if request.method == "POST" and len(request.form['comment']):
        comment = request.form['comment']
        dateEdited = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        cursor = db.cursor()
        cursor.execute("UPDATE COMMENT SET Comment = (%s), DatePosted = (%s) WHERE CommentID = (%s)", (comment, dateEdited, commentID))
        db.commit()
        cursor.close()
        gc.collect()
        isbn = session['isbn']
        return redirect(url_for('view_and_comment_book', isbn=isbn))
    elif comment_user != session['username']:
        error = "Not found!"
    return render_template('edit_book.html', comment=comment, error=error)

@app.route('/result', methods=['GET', 'POST'])
@login_required
def search_result():
    if request.method == "POST" and len(request.form['search']) > 0:
        search = request.form['search']
        cursor  = db.cursor()
        search           = cursor.execute("SELECT * FROM BOOK WHERE Title or AuthorName LIKE %s", ('%' + search + '%'))
        search_result    = cursor.fetchall()
        cursor.close()
        gc.collect()
        return render_template('result.html', results=search_result, found=search)
    else:
        return redirect('/dashboard')

if __name__ == "__main__":
    app.run(debug=True)
