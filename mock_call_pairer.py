from flask import (
    request, render_template,
    Flask, session, current_app,
    g
)
from flask_apscheduler import APScheduler
from utils import gen_pairs, update_file, read_file
from dotenv import load_dotenv
from pytz import utc
import time
import pprint
import os
import requests

import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


app = Flask(__name__)

sched = APScheduler()
sched.init_app(app)

@sched.task('interval', id='refresh_pairings', minutes=1, max_instances=1)
def refresh_pairings():
    update_file()

sched.start()

@app.get('/')
def root():
    pairs = read_file()
    if not pairs:
        print('Generating pairs...')
        pairs = read_file()
    return render_template('index.html', pairs=pairs)


@app.get('/refresh')
def rfsh():
    res = gen_pairs()

    return 'ok', 200

if __name__ == '__main__':
    app.run(debug=True, port=5050)
