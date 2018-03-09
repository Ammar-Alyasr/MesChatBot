import json,os
import time, locale

'''
def edits():
    dosya = open('arabalar.json', 'a')
    dosya.write('{"citys":' + '{' + '"yeri"' + ':' + '"' + 'iii' + '"' + ',' + '"numarasi"' +
                ':' + '"' + 'conv' + '"' + ',' + '"zaman"' + ':' + '"' + time.strftime(
        "%H:%M:%S") + '"' + ',' + '"yukseklikleri"' + ':' + '11' + '}}' + '\n')
    dosya.close()
'''
def weite_to_json(sender_id):
    dosya = open('arabalar.json', 'a')
    dosya.write('"' + sender_id + '" ' + '\n''')
    dosya.close()

