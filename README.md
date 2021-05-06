# Book Review 

![Project Image](https://drive.google.com/uc?export=view&id=1qIor_wxBUjl5bU5AYG3oPg5NS7Rx2sIR)

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)
- [License](#license)
- [Author Info](#authors)

---

## Description

This book review application allows users to register and log into the account. After logging in, users will be able to change password, change profile picture, view all books available on the database, rate and comment on books, edit and delete comments, search for books/authors, and log out of the program. 

#### Technologies

- Python 3 (version 3.8.5)
- Pymysql
- AWS RDS (MySQL engine)
- Flask (version 1.1.1)
- Flask-WTF
- Passlib
- Bootstrap 4

[Back To The Top](#Book-Review)

---

## How To Use

#### Installation
1. Clone the project to your local repository
```git
$ git clone https://github.com/ktruong29/project-362.git
```
2. Add 'execute' permission to `pkgs.sh`
```shell
$ chmod +x pkgs.sh
$ ./pkgs.sh
```

#### Prerequisites
- VM running Ubuntu 20.04
- Create an AWS account 
- Create RDS instance (MySQL engine)
- Modify the endpoint address in `app.py`

#### API Reference - Register an account

```python
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

            #Checking for duplicate usernames
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
```
[Back To The Top](#book-review)

---

## References

Flask - https://flask.palletsprojects.com/en/1.1.x/

Flask-WTF - https://flask-wtf.readthedocs.io/en/stable/

PyMySql - https://pypi.org/project/PyMySQL/ 

Passlib - https://passlib.readthedocs.io/en/stable/ 

Setting up AWS RDS - https://www.youtube.com/watch?v=Ng_zi11N4_c

Flask Web tutorial - https://pythonprogramming.net/practical-flask-introduction/

Bootstrap - https://getbootstrap.com/


[Back To The Top](#book-review)

---

## License

MIT License


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back To The Top](#book-review)

---

## Authors
- Kien Truong
- Sijie Shang
- Yao Lin

[Back To The Top](#book-review)
