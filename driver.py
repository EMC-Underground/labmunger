from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
from flask import Flask
from datetime import datetime
import methods
import os
import time

app = Flask(__name__)
scheduler = BackgroundScheduler()
port = int(os.getenv('VCAP_APP_PORT', 8080))

@app.route('/')
def index_route():
  return 'Welcome to the labmunger api'

if __name__ == '__main__':
  scheduler.add_job(methods.get_message_from_SQS, 'interval', seconds = 3)
  scheduler.add_listener(methods.error_listener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
  scheduler.start()

  try:
    app.run(host='0.0.0.0', port=port)

  except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
