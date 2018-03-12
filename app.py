import os
import sys
import json

from Sources.basket_process import  check_file, read_basket
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

                            if message_text == "Sepetem":
                                # user wanna view the basket
                                send_message(sender_id, "Sepetenizdekiler")
                                # read baskets items and send it to the user as list
                                basket = read_basket(sender_id)
                                send_message(sender_id, str(basket))

                            elif message_text == "Devam":
                                send_multi_template(sender_id)
                            else:
                                send_message(sender_id,  message_text)
                                send_multi_template(sender_id)

                        elif 'attachments' in messaging_event['message']:
                            send_image(sender_id, "http://thecatapi.com/api/images/get?format=src&type=gif")
                            if sender_id == "1668676606538319":
                                send_message('1668676606538319', "Hello ammarik")

                    if messaging_event.get("postback"):
                        if messaging_event['postback']['payload'] == "kahve_ekle":
                            # check_file: check if the user has own file, if not great it and add KAHVE
                            if check_file(sender_id, "kahve", 1):
                                send_message(sender_id, "Sepetinize bir kahve ekledim")
                                log("add new order into json data")
                            send_quick_replie(sender_id)

                        if messaging_event['postback']['payload'] == "cay_ekle":
                            if check_file(sender_id, "cay", 1):
                                send_message(sender_id, "Sepetinize bir cay ekledim")
                                log("add new order into json data")
                            send_quick_replie(sender_id)

                        if messaging_event['postback']['payload'] == "doner_ekle":
                            if check_file(sender_id, "doner", 1):
                                send_message(sender_id, "Sepetinize bir döner ekledim")
                                log("add new order into json data")
                            send_quick_replie(sender_id)

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
          "recipient": {
            "id":recipient_id
          },
          "message":{
            "attachment": {
              "type":"image",
              "payload": {
                "url": imag,
              }
            }
          }

          })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
'''

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
'''

def send_multi_template(recipient_id):
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
                #start menu of template
                "elements": [{

                    #firest
                    "title": "Tavuk Döner",
                    "subtitle": "Soslu Turşulu Tavuk Döner",
                    "image_url": "https://gimmedelicious.com/wp-content/uploads/2018/02/Buffalo-Chicken-Wraps-2.jpg",

                    #buttonus of menu
                    "buttons": [{
                        "type": "postback",
                        "title": "Sepete Ekle (3 Marka)",
                        "payload": "doner_ekle"
                    }, ],
                }, {
                    #second
                    "title": "Çay",
                    "image_url": "http://haberkibris.com/images/2014_12_14/isyerinde-cay-molasi-faydali--2014-12-14_m.jpg",
                   
                    #buttonus of menu
                    "buttons": [{
                        "type": "postback",
                        "title": "Sepete Ekle (1 Marka)",
                        "payload": "cay_ekle",
                    },],
                },  {
                    #3d menu
                    "title": "Kahve",
                    "image_url": "https://foto.sondakika.com/haber/2017/12/05/dunya-turk-kahvesi-gunu-nde-kahveniz-kahve-10314099_6526_o.jpg",
           
                    #buttonus of menu
                    "buttons": [{
                        "type": "postback",
                        "title": "Sepete Ekle (3 Marka)",
                        "payload": "kahve_ekle",
                    },],
                }]
            }
        }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_quick_replie(recipient_id):
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
            "text": "Tamamlamak istiyor musunuz:?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Sepetem",
                    "payload": "quick_yes",
                    "image_url":"http://www.dickson-constant.com/medias/images/catalogue/api/5477-logo-red-zoom.jpg"
                },
                {
                    "content_type": "text",
                    "title": "Devam",
                    "payload": "quick_continue",
                    "image_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/2000px-Solid_green.svg.png"
                }
            ]
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
