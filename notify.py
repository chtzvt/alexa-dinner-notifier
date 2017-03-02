import urllib2
import urllib
import json
import random
import base64


CONFIG = {
    'APP_ID': 'amzn1.ask.skill.[...]',
    'ACC_SID': ' ', # Your Twilio Account SID
    'AUTH_TOKEN': ' ', # Your Twilio Account Auth Token
    'TO_NUMBERS': ["5550100","5550199","5550120"], # Add your phone numbers to this array
    'FROM_NUMBER': " ", # Your Twilio account From number
    'MESSAGES': ["It's dinnertime!", "Time for dinner!", "Come down for dinner!", "Dinner is ready!"]
}


def handler(event, context):
    checkApplicationID(event['session']['application']['applicationId']);

    if (event['request']['intent']['name'] == "SendNotification"):
        for num in CONFIG['TO_NUMBERS']:
		   sendSMS(num, getNotificationContent())
        return generateJSON()
    else:
        raise ValueError("Invalid intent: " + event['request']['intent']['name'])


def sendSMS(num, msg):
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-agent': 'amazonaws-dinnerNotifier/1.0',
        'Authorization': 'Basic ' + base64.b64encode(CONFIG['ACC_SID'] + ':' + CONFIG['AUTH_TOKEN'])
    }
    message = {
        'To': num,
        'From': CONFIG['FROM_NUMBER'],
        'Body': msg,
    }
    req = urllib2.Request('https://api.twilio.com/2010-04-01/Accounts/' + CONFIG['ACC_SID'] + '/Messages', data=urllib.urlencode(message), headers=head)
    try:
        urllib2.urlopen(req)
    except:
        pass # We ignore HTTP exceptions, but you may choose not to do this

def getNotificationContent():
    return random.choice(CONFIG['MESSAGES'])


def generateJSON():
    return {
      "version": "1.0",
      "response": {
        "outputSpeech": {
          "type": "PlainText",
          "text": "OK, I'll put the word out."
        },
        "card": {
          "content": "Everyone knows it's time for dinner.",
          "title": "Dinner Notifier",
          "type": "Simple"
        },
        "shouldEndSession": True
      },
      "sessionAttributes": {}
    }


def checkApplicationID(id):
    if (id != CONFIG['APP_ID']):
      raise ValueError("Calling App ID does not match whitelist!")
