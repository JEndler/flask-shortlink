#!/usr/bin/env python3
# https://github.com/JEndler/flask-shortlink.git

from flask import Flask, render_template, request, redirect, url_for, Request
import shelve
from random import choice
from string import ascii_lowercase
import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Length, URL
from os import urandom

app = Flask(__name__, template_folder="templates", static_folder="static")
URL_SHELVE_PATH = 'urls.shelve'
ANALYTICS_SHELVE_PATH = 'analytics.shelve'
DEBUG = True
app.config['SECRET_KEY'] = urandom(32)
BASE_URL = "https://sl.s2s-bonn.de"


class ShortlinkForm(FlaskForm):
    url = StringField('URL', validators=[
        URL(require_tld=True, message='Invalid URL'),
        Length(max=1000, message='Maximum URL length exceeded!')])
    submit = SubmitField('Shorten!')


@app.route('/', methods=["GET", "POST"])
def root():
    form = ShortlinkForm()
    shortlink_url = None
    if request.method == "POST" and form.validate_on_submit():
        url = form.url.data
        _debug(url)
        id = _create_shortlink(url)
        shortlink_url = BASE_URL + url_for('get_url', id=id)
        form.url.data = ''
    return render_template("index.html", form=form, url=shortlink_url)


@app.route('/<id>')
def get_url(id: str):
    url = _lookup_url(id)
    if url is None:
        return redirect(url_for(root))
    _updateData(request, id)
    return redirect(url)


@app.route('/analytics/<id>')
def analytics(id):
    data = _prepareData(id)
    return render_template("analytics.html", total_visits=len(_loadData(id)), timeseries_data=data)


@app.route('/analytics')
def analytics_index():
    linklist = _loadShortlinks()
    return render_template('analytics_index.html', linklist=linklist)


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
        data = shelf[id]
        data.append({
            'timestamp': datetime.datetime.now(),
            'ip': request_ip,
            'user_agent': user_agent
        })
        shelf[id] = data


def _loadData(id: str):
    with shelve.open(ANALYTICS_SHELVE_PATH, 'r') as shelf:
        return shelf[id]


def _prepareData(id: str):
    # Format [yy-mm-dd, hits]
    # Format [Android_Hits, ect]
    data = _loadData(id)
    result = []
    for date in sorted(set([x['timestamp'].date() for x in data])):
        datestring = (str(date.year) + "-" + str(date.month) + "-" + str(date.day))
        visits = len([x['ip'] for x in data if x['timestamp'].date() == date])
        result.append((datestring, visits))
    return result


def _loadShortlinks():
    res = []
    with shelve.open(URL_SHELVE_PATH, 'r') as shelf:
        for key in shelf.keys():
            res.append((str(BASE_URL + '/' + str(key)), shelf[key], (str(BASE_URL + '/analytics/' + str(key)))))
    return res


def _debug(s):
    if DEBUG:
        print("Shortlink: " + s)


def main():
    print(_prepareData("img"))
    app.run('localhost')


if __name__ == '__main__':
    main()
