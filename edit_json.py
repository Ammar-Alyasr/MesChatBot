import json,os
import time, locale

def edits():
    dosya = open('arabalar.json')
    for doc in dosya:
        veriler = json.loads(doc)
        print(veriler)
    dosya.close()

def write_to_json(sender_id):
    if os.path.exists("arabalar.json"):
        dosya = open('arabalar.json', 'a')
        dosya.write('"' + str(sender_id) + '" ' + '\n''')
        dosya.close()

''' dosya.write('{"citys":' + '{' + '"yeri"' + ':' + '"' + 'iii' + '"' + ',' + '"numarasi"' +
                ':' + '"' + 'conv' + '"' + ',' + '"zaman"' + ':' + '"' + time.strftime(
        "%H:%M:%S") + '"' + ',' + '"yukseklikleri"' + ':' + '11' + '}}' + '\n')
        '''