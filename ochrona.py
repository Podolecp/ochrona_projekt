# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request, session
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Base, Log
from flask import request
import HTMLParser
import time
import json
app = Flask(__name__)
#notatki = [{'nick': 'Karol', 'data':'Zabijajo mnie utopcy :/'}, {'nick': 'Karol','data':'Zabijajo mnie nekkery :/'}]
#Tu stawiam baze danych
engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
sessiondb = DBSession()
#===================================

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
h = HTMLParser.HTMLParser()

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

def check_user(login, password):
    usertmp = sessiondb.query(User).filter(User.username == login).first()
    if usertmp is None:
        return False
    return usertmp.check_password(password)

def get_my_ip():
    return request.remote_addr

@app.errorhandler(404)
def page_not_found(error):
    return "404 Takiej strony ni ma :P ", 404

@app.route('/comment', methods=['GET', 'POST'])
def commenting():
    if request.method == 'POST':
        login = session['login']
        comment = request.form['comment']
        password = request.form['password']
        if not check_user(login, password) or not check_allowing(password):
            return display_main(u'Niepoprawne hasło', login )
        if not check_allowing_ws(comment):
            return display_main(u'Niepoprawne dane', login )
        f = open('notes.txt', 'rw')
        notes = json.load(f)
        new = {'nick': login, 'data': comment}
        notes.insert(0, new)
        f.close()
        f = open('notes.txt', 'w')
        json.dump(notes, f)
        f.close()
    return display_main('', session['login'])

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
    f = open('notes.txt', 'r')
    notes = json.load(f)
    f.close()
    return render_template('main.html', info=note, navigation=notes)

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
    if check_user(login, password):
        log = time.strftime("%d/%m/%Y") + ' - ' + time.strftime("%H:%M:%S") + ' - ' + get_my_ip()
        new_log = Log(login, log)
        sessiondb.add(new_log)
        sessiondb.commit()
        session['login'] = login
        return display_main("zalogowano", login)
    return render_template('login.html', info=u'Niepoprawne dane')


if __name__ == '__main__':
    app.debug = True
    app.run()
