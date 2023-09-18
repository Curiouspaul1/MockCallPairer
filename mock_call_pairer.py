from flask import (
    request, render_template,
    Flask, session, current_app,
    g
)
from flask_apscheduler import APScheduler
from utils import (
    gen_pairs,
    update_file,
    read_file,
    get_topic
)
from dotenv import load_dotenv
from pytz import timezone
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

@sched.task(
    'cron',
    id='refresh_pairings',
    day_of_week='sun',
    max_instances=1,
    hour=0,
    timezone=timezone('Africa/Lagos')
)
def refresh_pairings():
    update_file()

sched.start()

@app.get('/')
def root():
    pairs = read_file()
    topic = get_topic()
    if not pairs:
        print('Generating pairs...')
        update_file()
        pairs = read_file()
    return render_template('index.html', pairs=pairs, topic=topic)


@app.get('/refresh')
def rfsh():
    topic = request.args.get('topic')
    if topic:
        with open('topic.txt', 'w') as file:
            file.write(topic)
    update_file()

    return 'ok', 200

@app.get('/change_topic')
def change_topic():
    topic = request.args.get('topic')
    if topic:
        with open('topic.txt', 'w') as file:
            file.write(topic)
    return 'ok', 200

if __name__ == '__main__':
    app.run(debug=True, port=5050)
