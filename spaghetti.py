import os
import requests
import json



with open('encoding.json', 'r') as f:
    str1 = f.read()
    data = json.loads(str1)
a = ''
with open("codes.txt", "a") as fle:
    for item in data['countries']:
        if item['title'] == 'Россия':
            for reg in item['regions']:
                if reg['title'] == 'Москва и Московская область':
                    for sets in reg['settlements']:
                        #print(sets['title'])
                        if sets['title'] == 'Долгопрудный':
                            for st in sets['stations']:
                                #print(st['transport_type'], st['title'], st['codes'])
                                if st['transport_type'] == 'train':
                                    string1 = "'"+st['title'].lower()+"'"+': ' + "'"+st['codes']['yandex_code']+ "'"+', '
                                    #fle.write(string1)
                                    a = a + string1

print(a)


# for sets in data["countries"]['regions']['settlements']:
#     print(sets['title'])
#     if sets['title'] == 'Долгопрудный':
#         print(sets['stations'])


