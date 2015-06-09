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
from  sqlalchemy.sql.expression import func, select
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

@app.route('/settings', methods=['GET', 'POST'])
def display_settings():
    login = session['login']
    return render_template('settings.html', name=login)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    login = session['login']
    if request.method == 'POST':
        password = request.form['oldpassword']
        newpassword = request.form['newpassword']
        newpassword_repeat = request.form['newpassword_repeat']
    usertmp = sessiondb.query(User).filter(User.username == login).first()
    if usertmp is None:
        return render_template('settings.html', info='Jakis zly blad :(, przeloguj sie', name=login)
    if not check_allowing(password) or not check_allowing(newpassword) or not check_allowing(newpassword_repeat):
        return render_template('settings.html', info='Niepoprawne dane', name=login)
    if not newpassword == newpassword_repeat:
        return render_template('settings.html', info='Niepoprawne dane', name=login)
    if usertmp.check_password(password):
        usertmp.set_password(newpassword)
        return render_template('settings.html', info=u'Hasło zmienione', name=login)
    return render_template('settings.html', info='Niepoprawne dane', name=login)

@app.route('/show_logs', methods=['GET', 'POST'])
def show_logs():
    login = session['login']
    logs = sessiondb.query(Log).filter(Log.username==login).order_by(Log.id)
    return render_template('settings.html', name=login, logi=logs)

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
        f = open('notes.txt', 'r+')
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
    if not check_allowing(login) or not check_allowing(password) or not check_allowing(password2) or not check_allowing(question) or not check_allowing(answer):
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
    if not check_allowing(login) or not check_allowing(password):
        return render_template('login.html', info='Niepoprawne dane')
    if check_user(login, password):
        log = time.strftime("%d/%m/%Y") + ' - ' + time.strftime("%H:%M:%S") + ' - ' + get_my_ip()
        new_log = Log(login, log)
        sessiondb.add(new_log)
        sessiondb.commit()
        session['login'] = login
        return display_main("zalogowano", login)
    return render_template('login.html', info=u'Niepoprawne dane')

@app.route('/remind_password', methods=['GET', 'POST'])
def display_remind_password():
    return render_template('remind_password_login.html', info='')

@app.route('/remind_password_login', methods=['GET', 'POST'])
def remind_login():
    if request.method == 'POST':
        login = request.form['login']
    if not check_allowing(login):
        return render_template('remind_password_login.html', info='Niepoprawne dane')
    usertmp = sessiondb.query(User).filter(User.username == login).first()
    if usertmp is None:
        usertmp = sessiondb.query(User).order_by(func.random()).first()
        session['login_remind_legit'] = u'=^O^='
        session['login_remind'] = usertmp.username
        return render_template('remind_password.html', question=usertmp.question)
    session['login_remind_legit'] = u'=^-^='
    session['login_remind'] = login
    return render_template('remind_password.html', question=usertmp.question)

@app.route('/remind_password_answer', methods=['GET', 'POST'])
def remind_answer():
    login = session['login_remind']
    usertmp = sessiondb.query(User).filter(User.username == login).first()
    print usertmp.username
    if session['login_remind_legit'] == u'=^O^=':
        return render_template('remind_password.html', info='Niepoprawne dane', question=usertmp.question)
    if request.method == 'POST':
        answer = request.form['answer']
        newpassword = request.form['newpassword']
        newpassword_repeat = request.form['newpassword_repeat']
    if not newpassword == newpassword_repeat:
        return render_template('remind_password.html', info='Niepoprawne dane', question=usertmp.question)
    if not check_allowing(answer) or not check_allowing(newpassword) or not check_allowing(newpassword_repeat):
        return render_template('remind_password.html', info='Niepoprawne dane', question=usertmp.question)
    if usertmp is None:
        return render_template('remind_password.html', info='Niepoprawne dane', question=usertmp.question)
    if usertmp.check_answer(answer):
        usertmp.set_password(newpassword)
        return render_template('login.html', info=u'Hasło zmienione')
    return render_template('remind_password.html', info='Niepoprawne dane', question=usertmp.question)

if __name__ == '__main__':
    app.debug = True
    app.run()
