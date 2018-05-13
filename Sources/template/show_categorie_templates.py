import os

import requests
from flask import json

demli_cay = "https://i2.wp.com/www.kadinbakisi.com/wp-content/uploads/2017/08/demli-cayin-zararlari.jpg?resize=330%2C330"
cay = "http://www.ascihaber.com/v5/wp-content/uploads/2017/05/v5-1325764056_42_cay_-1.jpg"
kahve = "https://www.dogaldangelsin.com/image/cache/data/turk-kahvesi-800x800.jpg"
limonlu_cay = "http://trthaberstatic.s3-website-eu-west-1.amazonaws.com/resimler/372000/372908.jpg"
fincan_cay = "http://www.kazanabil.com/pasabahce-vela-12-parca-fincan-takimi-5258-11807-52-B.jpg"
bitki_cay = "https://www.pirelikedi.com/wp-content/uploads/2017/11/karisik-bitki-cayi-adet-sancisi.jpg"
su = "http://www.bik.gov.tr/wp-content/uploads/2017/05/su.jpg"
soda = "https://cdnph.upi.com/svc/sv/upi_com/8041492971723/2017/1/ed977c35005a74ee81bf9b0dbd8b0c8a/Study-links-diet-soda-to-stroke-and-dementia-risks.jpg"
nescafe = "http://cdn.shopify.com/s/files/1/1162/6052/products/product-image-mug_3_1024x1024.png?v=1520464037"
ada = "http://egebakkaliyesi.com/image/cache/catalog/yayla-ada-cayi-01-500x500.JPG"
kekik = "https://cdn.yemek.com/mncrop/940/625/uploads/2015/04/kekik-cayi-e1448290495871.jpg"
ihlamur = "http://ihlamur.gen.tr/images/ihlamur-cayi-nasil-yapilir.jpg"

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
                        "image_url": cay,

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
                        "image_url": kahve,

                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Ürünleri Getir",
                            "payload": "coffee_categorie",
                        },
                        ],
                    },
                        {
                        # 3d menu
                        "title": "Bitki Çay",
                        "image_url": bitki_cay,
                        # buttonus of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Ürünleri Getir",
                            "payload": "bitki_categorie",
                        },
                        ],
                    },
                        {
                            # 4th menu
                            "title": "Su",
                            "image_url": su,
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
                            "image_url": soda,
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
                    "top_element_style": "compact",
                    # start menu of template
                    "elements": [{
                        # first
                        "title": "Çay",
                        "subtitle": "Normal Çay",
                        "image_url": cay,
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
                        "image_url": demli_cay,

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
                        "image_url": limonlu_cay,

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
                            "image_url": fincan_cay,
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



def show_coffee(recipient_id):
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
                    "top_element_style": "compact",
                    # start menu of template
                    "elements": [{
                        # first
                        "title": "Sade Kahve",
                        "image_url": kahve,
                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_sade_coffee"
                        }, ],
                    },
                        {
                        # second
                        "title": "Orta Kahve",
                        "image_url": kahve,

                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_orta_kahve",
                        },
                        ],
                    },
                        {
                        # 3d menu
                        "title": "Şekerli Kahve",
                        "image_url": kahve,

                        # buttonus of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_sekerli_kahve",
                        },
                        ],
                    },
                        {
                            # 4th menu
                            "title": "Nescafe",
                            "image_url": nescafe,
                            # buttonus of menu
                            "buttons": [{
                                "type": "postback",
                                "title": "Sepeteye Ekle",
                                "payload": "add_nescafe",
                            },
                            ],
                    },
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def show_bitki(recipient_id):
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
                    "top_element_style": "compact",
                    # start menu of template
                    "elements": [{
                        # first
                        "title": "Keik Çayı",
                        "image_url": kekik,
                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_kekik_tea"
                        }, ],
                    },
                        {
                        # second
                        "title": "Ada Çayı",
                        "image_url": ada,

                        # buttons of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_ada_tea",
                        },
                        ],
                    },
                        {
                        # 3d menu
                        "title": "İhlamur Çayı",
                        "image_url": ihlamur,

                        # buttonus of menu
                        "buttons": [{
                            "type": "postback",
                            "title": "Sepeteye Ekle",
                            "payload": "add_ihlamur_tea",
                        },
                        ],
                    },
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)