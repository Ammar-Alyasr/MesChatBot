import json
import os

import Sources.template.show_categorie_templates as links
import requests

demli_cay = "https://i2.wp.com/www.kadinbakisi.com/wp-content/uploads/2017/08/demli-cayin-zararlari.jpg?resize=330%2C330"
cay = "http://www.ascihaber.com/v5/wp-content/uploads/2017/05/v5-1325764056_42_cay_-1.jpg"

def check_file(sender_id, order, pieces):
    # check if there is any file belong to that user_id
    if os.path.isfile('data\\users_temporary_data\\%s.json' % sender_id):
        add_order_to_basket(sender_id, order, pieces)
        return 1
    else:
        h = open('data\\users_temporary_data\\%s.json' % sender_id, 'w')
        data = '{"sender_id": "' + sender_id + '", "basket": [{}]}'
        h.write(str(data))
        h.close()
        add_order_to_basket(sender_id, order, pieces)
        return 1


def add_order_to_basket(sender_id, order, pieces):
    jim = json.load(open('data\\users_temporary_data\\%s.json' % sender_id))
    jim["basket"][0][str(order)] = str(pieces)

    # burada, en son hangi urun secildi ile ilgili bayrak koyuoruz
    # cunku buna gore adetini soracam,
    # ona direk 'basket' dizisine eklyebilirim aslinda...
    '''
    for i in jim["basket"][0]:
        i["sira_nerede"] == 
    '''
    jim["basket"][0]["sira_nerede"] = str(order)
    with open('data\\users_temporary_data\\%s.json' % sender_id, 'w') as outfile:
        json.dump(jim, outfile)

def check_last_order(sender_id, number):
    jim = json.load(open('data\\users_temporary_data\\%s.json' % sender_id))
    order = jim["basket"][0]

    for i in jim["basket"]:
        if i["sira_nerede"] == "çay":
            order["çay"] = number
        elif i["sira_nerede"] == "demli çay":
            order["demli_cay"] = number
        elif i["sira_nerede"] == "limonlu çay":
            order["limonlu çay"] = number
        elif i["sira_nerede"] == "fincan çay":
            order["fincan çay"] = number

        elif i["sira_nerede"] == "sade kahve":
            order["sade kahve"] = number
        elif i["sira_nerede"] == "orta kahve":
            order["orta kahve"] = number
        elif i["sira_nerede"] == "şekerli kahve":
            order["şekerli kahve"] = number
        elif i["sira_nerede"] == "nescafe":
            order["nescafe"] = number

        elif i["sira_nerede"] == "ada çayı":
            order["ada çayı"] = number
        elif i["sira_nerede"] == "kekik çayı":
            order["kekik çayı"] = number
        elif i["sira_nerede"] == "ihlamur çayı":
            order["ihlamur çayı"] = number

        elif i["sira_nerede"] == "soğuk su":
            order["soğuk su"] = number
        elif i["sira_nerede"] == "su":
            order["su"] = number

        with open('data\\users_temporary_data\\%s.json' % sender_id, 'w') as outfile:
            json.dump(jim, outfile)


def read_basket(sender_id):
    if os.path.isfile('data\\users_temporary_data\\%s.json' % sender_id):
        jim = json.load(open('data\\users_temporary_data\\%s.json' % sender_id))

        dict = jim["basket"][0]
        dict.pop("sira_nerede")
        asil = []
        for i in dict:
            if i == "cay":
                link = cay
            else:
                link = demli_cay
            kalip = {
                # first
                "title": "",
                "subtitle": "" + " adet",
                "image_url": link,
                # buttons of menu
                "buttons": [{
                    "type": "postback",
                    "title": "Sepeteden Çıkar",
                    "payload": "remove" + ""
                }]}

            kalip["title"] = i
            kalip["subtitle"] = dict[i] + " adet"
            asil.append(kalip)
        show_basket(asil, sender_id)

    else:
        return "Sepetiniz boş."


def show_basket(elements, recipient_id):
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
                    "elements": elements,
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

