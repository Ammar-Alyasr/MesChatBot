import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message

                try:
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    if messaging_event.get('message'):  # someone sent us a message
                        if 'text' in messaging_event['message']:
                            message_text = messaging_event["message"]["text"]  # the message's text
                            send_message(sender_id,  message_text)

                        elif 'attachments' in messaging_event['message']:
                            send_image(sender_id, "http://thecatapi.com/api/images/get?format=src&type=gif")
                            if sender_id == "1668676606538319":
                                send_message('1668676606538319', "Hello ammarik")

                    if messaging_event.get("postback"):
                        if messaging_event['postback']['payload'] == "bunu":
                            send_message(sender_id,"Bunu mu istediniz Simdi gel")

                        if messaging_event['postback']['payload'] == "dersinix":
                            send_message(sender_id,"Buna ne dersiniz Simdi gel")
                        if messaging_event['postback']['payload'] == "template":
                            send_message(sender_id, "Menu eklendi")
                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    
                except Exception:
                    send_message(sender_id, "sen ne attin ya!!!!")

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            attachment: {
            type: 'template',
            payload: {
            template_type: 'generic',
            elements: [
                {
                    title: '24th Street',
                    'subtitle': '43 mins, 9 cars. 58 mins, 9 cars. 73 mins, 9 cars.'
                },
                {
                    title: 'Daly City',
                    'subtitle': '43 mins, 9 cars. 58 mins, 9 cars. 73 mins, 9 cars. 1 min, 9 cars. 4 mins, 9 cars.'
                },
                {
                    title: 'Millbrae',
                    'subtitle': '8 mins, 4 cars. 23 mins, 4 cars. 38 mins, 4 cars. 13 mins, 5 cars.'
                }
            ]
        }
    }
    }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_image(recipient_id, imag):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
          "recipient":{
            "id":recipient_id
          },
          "message":{
            "attachment":{
              "type":"image",
              "payload":{
                "url":imag,
              }
            }
          }

          })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_general_template(recipient_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json",
    }
    data = json.dumps({
          "recipient": {
            "id": recipient_id
          },
          "message": {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": "islemi seciniz ",
                "buttons": [
                {
                "type": "postback",
                "title": "1 mi ?",
                "payload": "bir_secildi"
                },
                {
                "type": "postback",
                "title": "2 mi ?",
                "payload": "iki_secildi"
            }
        ]
      }
    }
  }
})

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
