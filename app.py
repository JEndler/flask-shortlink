#!/usr/bin/env python3
# https://github.com/JEndler/flask-shortlink.git

from flask import Flask, render_template, request, redirect, url_for, Request
import shelve
from random import choice
from string import ascii_lowercase
import datetime
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField, StringField
from wtforms.validators import Length, URL

app = Flask(__name__, template_folder="templates")
URL_SHELVE_PATH = 'urls.shelve'
ANALYTICS_SHELVE_PATH = 'analytics.shelve'
DEBUG = True


class ShortlinkForm(FlaskForm):
    url = StringField('URL', validators=[
        URL(require_tld=True, message='Invalid URL'),
        Length(max=1000, message='Maximum URL length exceeded!')])
    submit = SubmitField('Shorten!')


@app.route('/', methods=["GET", "POST"])
def root():
    if request.method == "POST":
        pass
    return render_template("index.html")


@app.route('/<id>')
def get_url(id: str):
    url = _lookup_url(id)
    if url is None:
        return redirect(url_for(root))
    _updateData(request, id)
    return redirect(url)


@app.route('/analytics/<id>')
def analytics():
    pass


def _create_shortlink(url: str) -> str:
    id = _make_id(url)
    with shelve.open(URL_SHELVE_PATH, 'c') as shelf:
        shelf[id] = url
    with shelve.open(ANALYTICS_SHELVE_PATH, 'c') as shelf:
        shelf[id] = []
    return id


def _make_id(url: str, id_len: int = 3) -> str:
    return ''.join(choice(ascii_lowercase) for n in range(id_len))


def _lookup_url(id: str) -> str:
    with shelve.open(URL_SHELVE_PATH, 'r') as shelf:
        try:
            return shelf[id]
        except Exception as e:
            _debug(str(e))
            return None


def _updateData(request: Request, id: str):
    request_ip = request.remote_addr
    user_agent = request.user_agent.platform
    with shelve.open(ANALYTICS_SHELVE_PATH, 'c') as shelf:
        shelf[id].append({
            'timestamp': datetime.datetime.now(),
            'ip': request_ip(),
            'user_agent': user_agent
        })


def _debug(s):
    if DEBUG:
        print("Shortlink: " + s)


def main():
    #print(_create_shortlink('http://jakobendler.eu'))
    print(_lookup_url('kra'))
    app.run('localhost')


if __name__ == '__main__':
    main()
