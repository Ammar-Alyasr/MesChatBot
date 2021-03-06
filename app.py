import os
import sys
import json

import Sources.basket_process as basket_process
from Sources.quick_replice.categorie_quick_replie import *
import Sources.template.show_categorie_templates as templates
import Sources.data.wit_response as nlp
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

                            intent = nlp.wit_response(messaging_event["message"]["nlp"]["entities"])
                            if intent != False:
                                if intent == "cay":
                                    templates.show_teas(sender_id)
                                elif intent == "kahve":
                                    templates.show_coffee(sender_id)
                                elif intent == "bitki":
                                    templates.show_bitki(sender_id)
                                elif intent == "su":
                                    templates.show_su(sender_id)
                                elif intent == "soda":
                                    templates.show_soda(sender_id)

                            else:
                                message_text = messaging_event["message"]["text"]  # the message's text

                                if message_text in numbers:
                                    basket_process.check_last_order(sender_id, message_text)

                                send_message(sender_id, "Yeniden Hosgeldiniz")
                                categorie_quick_replie(sender_id)

                        elif 'quick_reply' in messaging_event['message']:
                            # someone sent us a quick_reply
                            quick_reply = messaging_event["message"]["quick_reply"]["payload"]

                            if quick_reply == "categories":
                                # user want to view the categories
                                templates.categories_template(sender_id)

                            elif quick_reply == "view_basket":
                                # read baskets items and send it to the user as list just for now
                                basket = basket_process.read_basket(sender_id)

                                if str(basket) == "Sepetiniz boş.":
                                    send_message(sender_id, "Sepetinizde bir sey gözükmüyor")
                                    categorie_quick_replie(sender_id)
                                else:
                                    send_message(sender_id, basket)
                                    # BITIR question
                                    finishe_quick_replie(sender_id)

                            elif quick_reply == "finish_shopping":
                                basket_process.send_receipt(sender_id, sender_id)
                                send_message("1650134715044426", "Yeni Siparis var")
                                basket_process.send_receipt(sender_id, "1650134715044426")

                        elif 'attachments' in messaging_event['message']:
                            send_image(sender_id, "http://thecatapi.com/api/images/get?format=src&type=gif")
                            if sender_id == "1668676606538319":
                                send_message('1668676606538319', "Hello ammarik")

                    if messaging_event.get("postback"):
                        if messaging_event['postback']['payload'] == "add_tea":
                            if basket_process.check_file(sender_id, "çay", 1):
                                send_message(sender_id, "Sepetinize bir cay ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "veya")
                                categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "add_demli_cay":
                            if basket_process.check_file(sender_id, "demli çay", 1):
                                send_message(sender_id, "Sepetinize bir tene demli cay ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_limonlu_cay":
                            if basket_process.check_file(sender_id, "limonlu çay", 1):
                                send_message(sender_id, "Sepetinize bir tene limonlu çay ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_fincan_tea":
                            if basket_process.check_file(sender_id, "fincan çay", 1):
                                send_message(sender_id, "Sepetinize bir tene limonlu çay ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "add_sade_kahve":
                            if basket_process.check_file(sender_id, "sade kahve", 1):
                                send_message(sender_id, "Sepetinize bir tene sade kahve ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_orta_kahve":
                            if basket_process.check_file(sender_id, "orta kahve", 1):
                                send_message(sender_id, "Sepetinize bir tene orta kahve ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_sekerli_kahve":
                            if basket_process.check_file(sender_id, "şekerli kahve", 1):
                                send_message(sender_id, "Sepetinize bir tene şekerli kahve ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_nescafe":
                            if basket_process.check_file(sender_id, "nescafe", 1):
                                send_message(sender_id, "Sepetinize bir tene nescafe ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "add_ada_tea":
                            if basket_process.check_file(sender_id, "ada çayı", 1):
                                send_message(sender_id, "Sepetinize bir tene ada çayı ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_kekik_tea":
                            if basket_process.check_file(sender_id, "kekik çayı", 1):
                                send_message(sender_id, "Sepetinize bir tene kekik çay ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_ihlamur_tea":
                            if basket_process.check_file(sender_id, "ihlamur çayı", 1):
                                send_message(sender_id, "Sepetinize bir tene ihlamur çay ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "add_soguk_su":
                            if basket_process.check_file(sender_id, "soğuk su", 1):
                                send_message(sender_id, "Sepetinize bir tene soğuk su ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_su":
                            if basket_process.check_file(sender_id, "su", 1):
                                send_message(sender_id, "Sepetinize bir tene su ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "add_sade_soda":
                            if basket_process.check_file(sender_id, "sade soda", 1):
                                send_message(sender_id, "Sepetinize bir tene sade soda ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)
                        elif messaging_event['postback']['payload'] == "add_limonlu_soda":
                            if basket_process.check_file(sender_id, "limonlu soda", 1):
                                send_message(sender_id, "Sepetinize bir tene limonlu soda ekledim")
                                send_message(sender_id, "istediğiniz sipariş adetini girebilirsiniz")
                                send_message(sender_id, "ya da")
                                categorie_quick_replie(sender_id)

                        elif messaging_event['postback']['payload'] == "tea_categorie":
                            templates.show_teas(sender_id)
                        elif messaging_event['postback']['payload'] == "coffee_categorie":
                            templates.show_coffee(sender_id)
                        elif messaging_event['postback']['payload'] == "bitki_categorie":
                            templates.show_bitki(sender_id)
                        elif messaging_event['postback']['payload'] == "su_categorie":
                            templates.show_su(sender_id)
                        elif messaging_event['postback']['payload'] == "soda_categorie":
                            templates.show_soda(sender_id)
                        else:
                            send_message("1668676606538319", "Ne zaman devam edeceksin ammarcim")

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                except Exception as e:
                    send_message(sender_id, "sen ne attin ya!!!!" + str(e))

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


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)