# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request, session
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Base

app = Flask(__name__)

#Tu stawiam baze danych
engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
sessiondb = DBSession()
#===================================

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def check_allowing(str):
    for a in str:
        if a not in (string.letters + string.digits):
            return False
    return True

def check_allowing_ws(str):
    for a in str:
        if a not in (string.letters + string.digits + string.whitespace + '.,!?;:'):
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
            return display_main(u'Niepoprawne hasło', session['login'] )
        if not check_allowing_ws(comment):
            return display_main(u'Niepoprawne dane', session['login'] )
    return display_main('', session['login'] )

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
    note = note + " Witaj: " + login
    notes = open('notes.txt').read()
    return render_template('main.html', notes=notes, info=note)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password_repeat']
        question = request.form['secret_question']
        answer = request.form['answer']
    if not check_allowing(login) and not check_allowing(password) and not check_allowing(password2) and not check_allowing(question) and not check_allowing(answer):
        return render_template('register.html', info='Niepoprawne dane')
    if login == '' or password == '' or question == '' or answer == '':
        return render_template('register.html', info=u'Wypelnij wszystko')
    if not password2 == password:
        return render_template('register.html', info=u'Niepoprawne dane')
    usertmp = sessiondb.query(User).filter(User.username == login).first()
    if not usertmp is None:
        return render_template('register.html', info=u'Niepoprawne dane')
    new_user = User(login,password,question,answer)
    sessiondb.add(new_user)
    sessiondb.commit()
    return render_template('login.html', info=u'Coś tam coś rejestracja udana')

@app.route('/login', methods=['GET', 'POST'])
def veryfication():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
    if not check_allowing(login) and not check_allowing(password):
        return render_template('login.html', info='Niepoprawne znaki')
    usertmp = sessiondb.query(User).filter(User.username == login).first()
    if usertmp is None:
        return render_template('login.html', info=u'Niepoprawne dane')
    if usertmp.check_password(password):
        session['login'] = login
        return display_main("zalogowano", login)
    return render_template('login.html', info=u'Niepoprawne dane')


if __name__ == '__main__':
    app.debug = True
    app.run()
