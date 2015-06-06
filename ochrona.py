# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request

app = Flask(__name__)
message = ''


@app.errorhandler(404)
def page_not_found(error):
    return "404 Takiej strony ni ma :P", 404


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
    if login == 'Karol' and password == 'piczka':
        return render_template("main.html")
    return render_template('login.html', info='Niepoprawne dane (Karolek coś zepsuł)')


if __name__ == '__main__':
    app.debug = True
    app.run()
