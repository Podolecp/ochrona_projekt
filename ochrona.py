# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import string

app = Flask(__name__)
#Tu stawiam baze danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
#===================================


def check_allowing(str):
    for a in str:
        if a not in (string.letters or string.digits):
            return False
    return True

@app.errorhandler(404)
def page_not_found(error):
    return "404 Takiej strony ni ma :P " + error, 404


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html', info='')


@app.route('/main')
def display_main():
    return u'Shity i notatki'


@app.route('/login', methods=['GET', 'POST'])
def veryfication():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
    if not check_allowing(login) and not check_allowing(password):
        return render_template('login.html', info='Niepoprawne znaki')
    if login == 'Karol' and password == 'piczka':
        return render_template("main.html")
    return render_template('login.html', info=u'Niepoprawne dane (Karolek coś zepsuł)')


if __name__ == '__main__':
    app.debug = True
    app.run()
