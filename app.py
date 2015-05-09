#Import flask
from flask import Flask
from flask import render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import hashlib

#Library for bitmarket
from swaper import *


#Make app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Keys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.String(256), unique=False)
    private_key = db.Column(db.String(256), unique=True)
    url = db.Column(db.String(256), unique=True)

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.url = hashlib.sha256('{0.public_key}{0.private_key}lol'.format(self)).hexdigest()

    def __repr__(self):
        return "<Public:  {public} Prv: {private}, {url}>".format(
            public=self.public_key, private=self.private_key, url=self.url)


#Basic route for index
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/handle', methods=['GET', 'POST'])
def handle():
    if request.method == 'POST':
        if request.form['pubkey'] and request.form['privkey']:
            keys = Keys(request.form['pubkey'], request.form['privkey'])
            db.session.add(keys)
            db.session.commit()
            hashed_key = hashlib.sha256('{public_key}{private_key}lol'.format(public_key=request.form['pubkey'], private_key=request.form['privkey'])).hexdigest()
            return render_template("generated.html", hashed_key=hashed_key)
        else:
            return "Something wrong with data"
    else:
        return "Go to login page again, sorry"

@app.route('/display/<special>')
def display(special):
    #Query database for keys
    record = Keys.query.filter(Keys.url == special).first()
    #Class initialisation for bitmarket API
    yolo = Yolo(record.public_key, record.private_key)
    balance = str(yolo.get_balance())
    return render_template("display.html", balance=balance)

if __name__ == '__main__':
    app.run(debug=True)
