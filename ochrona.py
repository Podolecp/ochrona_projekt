# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)
message = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html', message = message)
@app.route('/main')
def display_main():
    return u'Shity i notatki'

@app.route('/login', methods=['GET', 'POST'])
def veryfication(login, password):
    if login == 'Karol' and password == 'piczka':
        render_template("main.html")
    message = 'Uncorrect login or password'
    index()
if __name__ == '__main__':
    app.debug = True
    app.run()
