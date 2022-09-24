# testing

import json
import myLibrary as lib

try:
    data = lib.loadJson('newSize.json')
    print(data[0]['size'])
    data[0]['size'] = 0
    lib.storeJson(data, 'newSize.json')
except:
    print('not true')
