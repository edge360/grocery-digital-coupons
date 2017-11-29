import sys
import flask
from flask import request
from flask import Response
from flask import jsonify
from flask import render_template
from flask import redirect
from flask_sslify import SSLify
import datetime
import base64
import hashlib
from threading import Thread
import grocery_coupons
from ConfigParser import RawConfigParser

app = flask.Flask(__name__)
sslify = SSLify(app)

data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods = ['POST'])
def post_collect():
    username = request.form.get('username')
    password = request.form.get('password')
    key = None

    if username and password:
        hasher = hashlib.sha1(username)
        key = base64.urlsafe_b64encode(hasher.digest()[0:20])

        if not key in data:
            # Set new user.
            data[key] = {
                'key': key,
                'username': username,
                'startDate': datetime.datetime.now(),
                'status': 'IDLE',
                'count': 0
            }

        if data[key]['status'] != 'RUNNING':
            # Run the method asynchronously.
            data[key]['status'] = 'RUNNING'
            thread = Thread(target=grocery_coupons.shoprite, args=(username, password, 10, onStatus, onComplete))
            thread.start()

    # Return an html or json view depending on the client.
    return redirect('/result/' + key if 'text/html' in request.headers.get('Accept') else '/collect/' + key) if key in data else jsonify({ 'status': 'MISSING LOGIN' })

@app.route('/collect/')
@app.route('/collect/<key>')
def get_collect(key=None):
    result = data[key] if key in data else {}

    if result and not result['status'] == 'RUNNING':
        # Delete the key, now that status has been returned.
        data.pop(key)

    return jsonify(result), 404 if result == {} else 200

@app.route('/result/')
@app.route('/result/<key>')
def status(key=None):
    username = None
    count = None
    screenshot = None
    startDate = None
    endDate = None
    done = False
    status = None
    message = None

    if key in data:
        username = data[key]['username']
        count = data[key]['count']
        status = data[key]['status'].lower() if 'status' in data[key] else None
        message = data[key]['message'] if 'message' in data[key] else None
        screenshot = data[key]['screenshot'] if 'screenshot' in data[key] else None
        startDate = data[key]['startDate']
        endDate = data[key]['endDate'] if 'endDate' in data[key] else data[key]['lastUpdate'] if 'lastUpdate' in data[key] else None
        done = True if 'endDate' in data[key] else False

        return render_template('result.html', **locals())
    else:
        return redirect('/')

def onComplete(result):
    # Get the key for the user.
    hasher = hashlib.sha1(result['email'])
    key = base64.urlsafe_b64encode(hasher.digest()[0:20])

    # Update the status with the result.
    data[key]['endDate'] = datetime.datetime.now()
    data[key]['status'] = 'IDLE'
    data[key]['count'] = result['count']
    data[key]['screenshot'] = result['screenshot']

def onStatus(text, email):
    global data

    # Get the key for the user.
    hasher = hashlib.sha1(email)
    key = base64.urlsafe_b64encode(hasher.digest()[0:20])
    print 'Using key ' + key

    # Update status.
    if key in data:
        data[key]['message'] = text
        data[key]['lastUpdate'] = datetime.datetime.now()

    print text

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)