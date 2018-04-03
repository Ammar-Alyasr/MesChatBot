import json
import os

import requests


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
    for i in jim["basket"][0]:
        if i["sira_nerede"] == "cay":
            jim["basket"][0]["cay"] = number
        with open('data\\users_temporary_data\\%s.json' % sender_id, 'w') as outfile:
            json.dump(jim, outfile)


def read_basket(sender_id):
    if os.path.isfile('data\\users_temporary_data\\%s.json' % sender_id):
        jim = json.load(open('data\\users_temporary_data\\%s.json' % sender_id))

        return jim["basket"]
    else:
        return "Sepetiniz boş."



'''
if add_to_basket("TEST_FILE_SON1", "cay"):
    print("Eklendi")

jim = json.load(open('TEST_FILE_SON1.json'))


aram = jim["data"][0]["siparisler"]
print(type(aram))
aram.append("yemek")
aram.append("blabla")
print(aram)
print(jim["data"][0])
with open('TEST_FILE_SON1.json', 'w') as outfile:
    json.dump(jim, outfile)
    
    
 
jim = json.load(open('TEST_FILE_SON1.json'))
print(jim["basket"][0]["cay"])
jim["basket"][0]["cay"] = "3"
print(jim["basket"][0]["cay"])

with open('TEST_FILE_SON1.json', 'w') as outfile:
    json.dump(jim, outfile)
'''