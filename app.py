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

                try:
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][
                        "id"]  # the recipient's ID, which should be your page's facebook ID

                    if messaging_event.get('message'):  # someone sent us a message
                        if 'text' in messaging_event['message']:
                            message_text = messaging_event["message"]["text"]  # the message's text
                            send_message(sender_id, "abi sen  " + message_text + " misin ??")
                            send_image_tamplate(sender_id)
                        elif 'attachments' in messaging_event['message']:
                            send_image(sender_id, "http://thecatapi.com/api/images/get?format=src&type=gif")
                            if sender_id != "1668676606538319":
                                send_message('1668676606538319', message_text + sender_id)
                    if messaging_event.get("postback"):
                        if messaging_event['postback']['payload'] == "bunu":
                            send_message(sender_id,"Bunu mu istediniz Simdi gel")

                        if messaging_event['postback']['payload'] == "dersinix":
                            send_message(sender_id,"Buna ne dersiniz Simdi gel")

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
            "text": message_text
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
        "Content-Type": "application/json"
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
                "title": "Bunu mu istediniz?",
                "payload": "bunu"
                },
                {
                "type": "postback",
                "title": "Buna da ne dersiniz?",
                "payload": "dersinix"
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

#adding picitures tamplates. it dosent work for now....
def send_image_tamplate(recipient_id):
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
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Welcome to Peter'\''s Hats",
                            "image_url": "https://i.kinja-img.com/gawker-media/image/upload/s--M7aOfgD_--/c_scale,fl_progressive,q_80,w_800/riufs7rtpk6okzrqiqmy.jpg",
                            "subtitle": "We'\''ve got the right hat for everyone.",
                            "default_action": {
                                "type": "https://developers.facebook.com",
                                "url": "https://i.kinja-img.com/gawker-media/image/upload/s--M7aOfgD_--/c_scale,fl_progressive,q_80,w_800/riufs7rtpk6okzrqiqmy.jpg",
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": "https://i.kinja-img.com/gawker-media/image/upload/s--M7aOfgD_--/c_scale,fl_progressive,q_80,w_800/riufs7rtpk6okzrqiqmy.jpg"
                            },
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Start Chatting",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                },
                            ]
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
