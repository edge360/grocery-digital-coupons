import sys
import subprocess
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
            thread = Thread(target=grocery_coupons.shoprite, args=(username, password, 10, onStatus))
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

def onStatus(status):
    global data

    # Get the key for the user.
    hasher = hashlib.sha1(status['email'])
    key = base64.urlsafe_b64encode(hasher.digest()[0:20])

    # Update status.
    if key in data:
        data[key]['count'] = status['count']
        data[key]['screenshot'] = status['screenshot']
        data[key]['message'] = status['message']
        data[key]['lastUpdate'] = datetime.datetime.now()
        if data[key]['message'] == 'Complete!':
            data[key]['status'] = 'IDLE'
            data[key]['endDate'] = datetime.datetime.now()

    print status['message']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'install' or sys.argv[1] == '-install' or sys.argv[1] == '--install' or sys.argv[1] == 'i' or sys.argv[1] == '-i' or sys.argv[1] == '--i':
            # Install dependencies.
            subprocess.call(['python', 'setup.py'])
    else:
        app.run(debug=True, use_reloader=True)
