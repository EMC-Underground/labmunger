import boto3
import xmltodict
import json
import requests
import os


lab_url = "http://labapi.bellevuelab.isus.emc.com/"
# Resources:
# - http://boto3.readthedocs.io/en/latest/guide/resources.html
def get_message_from_SQS():
  # Get the service resource
  sqs = boto3.resource('sqs')

  # Get the queue
  queue = sqs.get_queue_by_name(QueueName='lab_comm')

  messages = queue.receive_messages(MessageAttributeNames=['AmazonIntent'])
  # Process messages by printing out body and optional author name
  for message in messages:
    print("We got a message")
    # Get the custom author message attribute if it was set
    eventType = ""
    print (message)
    if message.message_attributes is not None:
      eventType = message.message_attributes.get('AmazonIntent').get('StringValue')
      print("The message was from Alexa and the intent is {0}".format(eventType))
      # event = json.loads(message.body)
      if eventType == "AllVMsCount":
        print('Need to count all of the vms')
        vm_count = fetch_vm_count()
        print("There are {0} vms in the lab".format(vm_count))
        response = sqs.get_queue_by_name(QueueName='lab_comm_2').send_message(MessageBody="There are {0} vms in the lab.".format(vm_count), MessageAttributes={"AmazonResponse":{"StringValue":eventType,'DataType': 'String'}})
        print(response)
        # Let the queue know that the message is processed
        message.delete()

def fetch_vm_count():
  vm_count = 0
  r = requests.get('{0}vms/'.format(lab_url))
  vms = r.json()['vm']
  vm_count = len(vms)
  return vm_count

# listener to give visibility into job completetion
def error_listener(event):
  if event.exception:
    print("The job failed...{0}".format(event.exception))
    print("{0}".format(event.traceback))
  else:
    print("The job worked!")
