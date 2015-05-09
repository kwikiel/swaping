#Import flask
from flask import Flask
from flask import render_template, request
#Make app instance
app = Flask(__name__)

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
        return request.form['pubkey']


if __name__ == '__main__':
    app.run(debug=True)
