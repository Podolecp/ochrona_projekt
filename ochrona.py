# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request

app = Flask(__name__)
message = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html', message='')
@app.route('/main')
def display_main():
    return u'Shity i notatki'

@app.route('/login', methods=['GET', 'POST'])
def veryfication():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        print 'w postcie'
    if login == 'Karol' and password == 'piczka':
        print 'karol piczka'
        return render_template("main.html")
    print 'niepoprawne dane'
    return render_template('login.html', messege='Niepoprawne dane')

if __name__ == '__main__':
    app.debug = True
    app.run()
