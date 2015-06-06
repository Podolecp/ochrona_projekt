# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return u'Ekran główny, tu będzie logowanie a Karol to PICZKA i zabijają go utopce :P'


if __name__ == '__main__':
    app.run()
