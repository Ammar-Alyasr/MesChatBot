import json
import os


def check_file(sender_id, order, pieces):
    # check if there is any file belong to the user_id
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
    print(jim)
    orders = jim["basket"][0]
    print(orders)
    jim["basket"][0][str(order)] = str(pieces)
    print(jim)
    with open('data\\users_temporary_data\\%s.json' % sender_id, 'w') as outfile:
        json.dump(jim, outfile)


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