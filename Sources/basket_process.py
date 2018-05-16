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

    if str(order) in jim["basket"][0]:
        jim["basket"][0][str(order)] += pieces
    else:
        jim["basket"][0][str(order)] = pieces

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
    try:
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

            elif i["sira_nerede"] == "sade soda":
                order["sade soda"] = number
            elif i["sira_nerede"] == "limonlu soda":
                order["limonlu soda"] = number

            with open('data\\users_temporary_data\\%s.json' % sender_id, 'w') as outfile:
                json.dump(jim, outfile)
    except:
        pass


def read_basket(sender_id):
    if os.path.isfile('data\\users_temporary_data\\%s.json' % sender_id):
        jim = json.load(open('data\\users_temporary_data\\%s.json' % sender_id))
        link = ""
        dict = jim["basket"][0]
        dict.pop("sira_nerede")
        asil = []

        for i in dict:
            if i == "çay":
                link = links.cay
            elif i == "demli çay":
                link = links.demli_cay
            elif i == "limonlu çay":
                link = links.limonlu_cay
            elif i == "fincan çay":
                link = links.fincan_cay
            elif i == "sade kahve" or i == "orta kahve" or i == "şekerli kahve":
                link = links.kahve
            elif i == "nescafe":
                link = links.nescafe
            elif i == "ada çayı":
                link = links.ada
            elif i == "kekik çayı":
                link = links.kekik
            elif i == "ihlamur çayı":
                link = links.ihlamur
            elif i == "soğuk su":
                link = links.soguk_su
            elif i == "su":
                link = links.su
            elif i == "sade soda":
                link = links.sade_soda
            elif i == "limonlu soda":
                link = links.limonlu_soda

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
            kalip["subtitle"] = str(dict[i])  + " adet"
            asil.append(kalip)
        show_basket(asil, sender_id)

    else:
        return "Sepetiniz boş."


def receipt_basket(sender_id):
    if os.path.isfile('data\\users_temporary_data\\%s.json' % sender_id):
        jim = json.load(open('data\\users_temporary_data\\%s.json' % sender_id))
        link = ""
        dict = jim["basket"][0]
        dict.pop("sira_nerede")
        asil = []

        for i in dict:
            if i == "çay":
                link = links.cay
            elif i == "demli çay":
                link = links.demli_cay
            elif i == "limonlu çay":
                link = links.limonlu_cay
            elif i == "fincan çay":
                link = links.fincan_cay
            elif i == "sade kahve" or i == "orta kahve" or i == "şekerli kahve":
                link = links.kahve
            elif i == "nescafe":
                link = links.nescafe
            elif i == "ada çayı":
                link = links.ada
            elif i == "kekik çayı":
                link = links.kekik
            elif i == "ihlamur çayı":
                link = links.ihlamur
            elif i == "soğuk su":
                link = links.soguk_su
            elif i == "su":
                link = links.su
            elif i == "sade soda":
                link = links.sade_soda
            elif i == "limonlu soda":
                link = links.limonlu_soda

            kalip = {
                # first
                "title" : "", #isim
                "subtitle" : "", # adet
                "price" : 2,
                "currency" : "USD",
                "image_url" : link
                }

            kalip["title"] = i
            kalip["subtitle"] = str(dict[i]) + " adet"
            asil.append(kalip)
            return asil


def send_receipt(sender_id):

    elements = receipt_basket(sender_id)
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient":{
        "id": sender_id
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"receipt",
            "recipient_name":"Ammarik",
            "order_number":"12345678902",
            "currency":"USD",
            "payment_method":"POS Cihazı",
            "order_url":"http://petersapparel.parseapp.com/order?order_id=123456",
            "timestamp":"1428444852",
            "address":{
              "street_1":"Kötekli Mh. Kyk Yurdu",
              "street_2":"5385294458",
              "city":"Muğla",
              "postal_code":"94025",
              "state":"Menteşe",
              "country":"Turkey"
            },
            "summary":{
              "subtotal":1.00,
              "shipping_cost":00,
              "total_tax":1.3,
              "total_cost":2.3
            },
            "elements": elements
          }
        }
      }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


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

