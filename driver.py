from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
import methods
import os

if __name__ == '__main__':
  scheduler.add_job(methods.get_message_from_SQS, 'interval', seconds = 10)
  scheduler.add_listener(methods.error_listener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
  scheduler.start()

  try:
    while True:
      time.sleep(2)
  except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
