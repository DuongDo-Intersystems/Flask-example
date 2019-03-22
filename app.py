from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint

app = Flask(__name__)
app.secret_key = "Duongyeudh"


@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/members")
def members():
    return "Members"


@app.route('/hello/<name>')
def hello_user(name):
    quotes = [
        "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
        "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
        "'To understand recursion you must first understand recursion..' -- Unknown",
        "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
        "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
        "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"
    ]
    random_number = randint(0, len(quotes) - 1)
    quote = quotes[random_number]
    # return render_template('test.html', name=name)
    return render_template(
        'test.html', name=name, quote=quote)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User {}'.format(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            # return redirect(url_for('index'))
    return render_template('form.html')


@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
       <form action = "/" method = "post">
          <p><input type = text name = username/></p>
          <p<<input type = submit value = Login/></p>
       </form>
       '''


@app.route('/main')
def main():
    if 'username' in session:
        username = session['username']
        return "'Logged in as {}'.format(username)  <a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in. <br><a href = '/signin'>click here to log in</b></a>"


@app.route('/signout')
def signout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run()
