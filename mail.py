from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dohoangduong95@gmail.com'
app.config['MAIL_PASSWORD'] = 'Duong1369'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def index():
    msg = Message('Hello', sender='dohoangduong95@gmail.com', recipients=['dhdo@csbsju.edu'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


if __name__ == '__main__':
    app.run()