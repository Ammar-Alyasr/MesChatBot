import os
import sys
import json


import Sources.basket_process as basket_process
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
                    recipient_id = messaging_event["recipient"]["id"]
                    # the recipient's ID, which should be your page's facebook ID

                    if messaging_event.get('message'):  # someone sent us a message
                        if 'text' in messaging_event['message'] and 'quick_reply' not in messaging_event['message']:
                            message_text = messaging_event["message"]["text"]  # the message's text

                            send_message(sender_id, "Yeniden Hosgeldiniz")
                            categorie_quick_replie(sender_id)

                        elif 'quick_reply' in messaging_event['message']:
                            # someone sent us a quick_reply
                            quick_reply = messaging_event["message"]["quick_reply"]["payload"]

                            if quick_reply == "categories":
                                # user want to view the categories
                                categories_template(sender_id)

                            elif quick_reply == "view_basket":
                                # read baskets items and send it to the user as list just for now
                                basket = basket_process.read_basket(sender_id)

                                if str(basket) == "Sepetiniz boş.":
                                    categorie_quick_replie(sender_id)
                                else:
                                    send_message(sender_id, str(basket))

                        elif 'attachments' in messaging_event['message']:
                            send_image(sender_id, "http://thecatapi.com/api/images/get?format=src&type=gif")
                            if sender_id == "1668676606538319":
                                send_message('1668676606538319', "Hello ammarik")

                    if messaging_event.get("postback"):
                        if messaging_event['postback']['payload'] == "kahve_ekle":
                            # check_file: check if the user has own file, if not great it and add KAHVE
                            if basket_process.check_file(sender_id, "kahve", 1):
                                send_message(sender_id, "Sepetinize bir kahve ekledim")
                            send_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "add_tea":
                            if basket_process.check_file(sender_id, "cay", 1):
                                send_message(sender_id, "Sepetinize bir cay ekledim")
                            categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "doner_ekle":
                            if basket_process.check_file(sender_id, "doner", 1):
                                send_message(sender_id, "Sepetinize bir döner ekledim")
                            send_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "tea_categorie":
                            show_teas(sender_id)
                        else:
                            send_message("1668676606538319", "Ne zaman devam edeceksin ammarcim")

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
            "id": recipient_id
          },
          "message": {
            "attachment": {
              "type": "image",
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
                    "payload": "view_basket",
                    "image_url": "http://www.dickson-constant.com/medias/images/catalogue/api/5477-logo-red-zoom.jpg"
                },
                {
                    "content_type": "text",
                    "title": "Devam",
                    "payload": "continue",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/2000px-Solid_green.svg.png"
                }
            ]
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def categories_template(recipient_id):
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
                    # start menu of template
                    "elements": [{
                        # first
                        "title": "Çay",
                        "subtitle": "şekerli/siz, açık normal, demli...",
                        "image_url": "https://gimmedelicious.com/wp-content/uploads/2018/02/Buffalo-Chicken-Wraps-2.jpg",

                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Ürünleri Getir",
                            "payload": "tea_categorie"
                        }, ],
                    },
                        {
                        # second
                        "title": "Kahveler",
                        "image_url": "http://haberkibris.com/images/2014_12_14/isyerinde-cay-molasi-faydali--2014-12-14_m.jpg",

                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Ürünleri Getir",
                            "payload": "cofee_categorie",
                        },
                        ],
                    },
                        {
                        # 3d menu
                        "title": "Bitki Çay",
                        "image_url": "https://foto.sondakika.com/haber/2017/12/05/dunya-turk-kahvesi-gunu-nde-kahveniz-kahve-10314099_6526_o.jpg",

                        # buttonus of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Ürünleri Getir",
                            "payload": "herbal_categorie",
                        },
                        ],
                    },
                        {
                            # 4th menu
                            "title": "Su",
                            "image_url": "https://foto.sondakika.com/haber/2017/12/05/dunya-turk-kahvesi-gunu-nde-kahveniz-kahve-10314099_6526_o.jpg",

                            # buttonus of menu
                            "buttons": [{
                                "type": "postback",
                                "title": "Ürünleri Getir",
                                "payload": "water_categorie",
                            },
                            ],
                        },
                        {
                            # 5th menu
                            "title": "Soda",
                            "image_url": "https://foto.sondakika.com/haber/2017/12/05/dunya-turk-kahvesi-gunu-nde-kahveniz-kahve-10314099_6526_o.jpg",

                            # buttonus of menu
                            "buttons": [{
                                "type": "postback",
                                "title": "Ürünleri Getir",
                                "payload": "soda_categorie",
                            },
                            ],
                        },

                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def show_teas(recipient_id):
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
                    "template_type": "list",
                    # compact or large
                    "top_element_style": "large",
                    # start menu of template
                    "elements": [{
                        # first
                        "title": "Çay",
                        "subtitle": "Normal Çay",
                        "image_url": "https://gimmedelicious.com/wp-content/uploads/2018/02/Buffalo-Chicken-Wraps-2.jpg",
                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_tea"
                        }, ],
                    },
                        {
                        # second
                        "title": "Demli Çay",
                        "image_url": "https://i2.wp.com/www.kadinbakisi.com/wp-content/uploads/2017/08/demli-cayin-zararlari.jpg?resize=330%2C330",

                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_demli_cay",
                        },
                        ],
                    },
                        {
                        # 3d menu
                        "title": "Limonlu Çay",
                        "image_url": "https://foto.sondakika.com/haber/2017/12/05/dunya-turk-kahvesi-gunu-nde-kahveniz-kahve-10314099_6526_o.jpg",

                        # buttonus of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_limonlu_cay",
                        },
                        ],
                    },
                        {
                            # 4th menu
                            "title": "Fincan Çay",
                            "image_url": "https://foto.sondakika.com/haber/2017/12/05/dunya-turk-kahvesi-gunu-nde-kahveniz-kahve-10314099_6526_o.jpg",

                            # buttonus of menu
                            "buttons": [{
                                "type": "postback",
                                "title": "Sepeteye Ekle",
                                "payload": "add_fincan",
                            },
                            ],
                        },

                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def categorie_quick_replie(recipient_id):
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
            "text": "Kategorileri görmek ister misiniz ? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Kategoriler",
                    "payload": "categories",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/2000px-Solid_green.svg.png"
                },
                {
                    "content_type": "text",
                    "title": "Sepetem",
                    "payload": "view_basket",
                    "image_url": "http://www.pvhc.net/img180/qzsenvtfibwdmkaipzij.png"
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