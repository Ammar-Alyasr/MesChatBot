import os
import json

import requests
from app import log


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
                        "subtitle": ":şekerli/siz, açık normal, demli...",
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
