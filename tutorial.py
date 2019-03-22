from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort
from werkzeug import secure_filename
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return "'Logged in as {}'.format(username)  <a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in. <br><a href = '/signin'>click here to log in</b></a>"


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/result',methods = ['POST', 'GET'])
def student_result():
    if request.method == 'POST':
        data = request.form
        return render_template("result.html", result=data)


@app.route('/cookie')
def cookie():
    return render_template('cookie.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)

    return resp


@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome '+name+'</h1>'


@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''

       <form action = "" method = "post">
          <p><input type = text name = username></p>
          <p><input type = submit value = Login></p>
       </form>

       '''


@app.route('/signout')
def signout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route('/enternew')
def new_student():
    return render_template('students.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, addr, city, pin) VALUES(?, ?, ?, ?)", (nm, addr, city, pin))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("records.html", msg=msg)
            con.close()


@app.route('/list')
def list_students():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
