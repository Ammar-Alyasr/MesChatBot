import json,os
import time, locale

def read_from_json():
    dosya = open('arabalar.json')
    for doc in dosya:
        veriler = json.loads(doc)

        return veriler
    dosya.close()

def write_to_json(sender_id):
    if os.path.exists("arabalar.json"):
        dosya = open('arabalar.json', 'a')
        dosya.write('"' + str(sender_id) + '" ' + '\n''')
        dosya.close()
        return 1


def oku():
    dosya = open('arabalar.json')
    data = json.load(dosya)

    data.append({'name': 'ahmet', 'login':'tdwo',"location":"berbgvvrebrebre"})

    for dt in data:
        if dt["name"]=='ahmet':
            print(dt["location"])

oku()

a = [{"name":"Luuk W.","login":"twinone","location":"Barcelona, Spain","join_date":"May 1, 2013","language":"Makefile","gravatar":"https://avatars0.githubusercontent.com/u/4309591?v=3&s=64","followers":48,"user_stars":"97","stars":22,"organizations":[],"contributions":12100}]
a.append({"name":"ahmetd"})



''' dosya.write('{"citys":' + '{' + '"yeri"' + ':' + '"' + 'iii' + '"' + ',' + '"numarasi"' +
                ':' + '"' + 'conv' + '"' + ',' + '"zaman"' + ':' + '"' + time.strftime(
        "%H:%M:%S") + '"' + ',' + '"yukseklikleri"' + ':' + '11' + '}}' + '\n')
        '''