# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request, session
from flask.ext.sqlalchemy import SQLAlchemy
import os
import string
import uzytkownik

app = Flask(__name__)
#Tu stawiam baze danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
#===================================

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def check_allowing(str):
    for a in str:
        if a not in (string.letters or string.digits):
            return False
    return True

@app.errorhandler(404)
def page_not_found(error):
    return "404 Takiej strony ni ma :P ", 404

@app.route('/comment', methods=['GET', 'POST'])
def commenting():
    if request.method == 'POST':
        comment = request.form['comment']
        password = request.form['password']
        if not check_allowing(password):
            return display_main(u'Niepoprawne hasło',session['login'] )
    return display_main('',session['login'] )

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'login' in session:
        return display_main(' ', session['login'])
    return render_template('login.html', info='')

@app.route('/registration', methods=['GET', 'POST'])
def display_registration():
    return render_template('register.html', info='')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('login', None)
    return index()

#@app.route('/main', methods=['GET', 'POST'])
def display_main(note, login):
    notes = """
    Witaj: """ + login + """
    Notatki Karola"""
    return render_template('main.html', notes=notes, info=note)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    print request.form['login'] + request.form['password'] + request.form['password_repeat'] + request.form['secret_question'] + request.form['answer']
    return render_template('register.html', info=u'Coś tam coś')

@app.route('/login', methods=['GET', 'POST'])
def veryfication():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
    if not check_allowing(login) and not check_allowing(password):
        return render_template('login.html', info='Niepoprawne znaki')
    usertmp = uzytkownik.User.query.filter_by(username=login).first()
    if usertmp is None:
        return render_template('login.html', info=u'Niepoprawne dane')
    if usertmp.check_password(password):
        session['login'] = login
        return display_main("zalogowano", login)
    return render_template('login.html', info=u'Niepoprawne dane')


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
