import os

import requests
from flask import json

numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

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
            "text": "Kategorileri görmek ister misiniz? ",
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


def finishe_quick_replie(recipient_id):
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
            "text": "siparisinizi tamamlayin",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Alışverişi Bitir",
                    "payload": "finish_shopping",
                    "image_url": "https://image.flaticon.com/icons/png/512/244/244590.png"
                },
                {
                    "content_type": "text",
                    "title": "Kategoriler",
                    "payload": "categories",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/2000px-Solid_green.svg.png"
                }
            ]
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

