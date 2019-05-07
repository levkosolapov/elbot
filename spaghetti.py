"""
# this file contains some utils that help us make
 a dictionary with codes (only with those we need) from encoding.json

"""
import os
import requests
import json
import re


# def dump_raspis(data):
#     jsondata = json.dumps(data)
#     with open("request.txt", "w") as f:
#         f.write(jsondata)


def write_codes_to_dictionary_in_a_txt_file():
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
                            # if sets['title'] == 'Долгопрудный':
                                for st in sets['stations']:
                                    #print(st['transport_type'], st['title'], st['codes'])
                                    if st['transport_type'] == 'train':
                                        string1 = "'"+st['title'].lower()+"'"+': ' + "'"+st['codes']['yandex_code']+ "'"+', '
                                        fle.write(string1)


# for sets in data["countries"]['regions']['settlements']:
#     print(sets['title'])
#     if sets['title'] == 'Долгопрудный':
#         print(sets['stations'])

def replace_all_goddamn_motherfucking_russian_ёs_because_everybody_hates_that_shitty_char():
    with open("codes.txt", "r+") as fle:
        our_goddamn_fucking_dictionary = fle.read()
        our_goddamn_fucking_dictionary = our_goddamn_fucking_dictionary.replace("ё", "е")
    with open("codes.txt", "w+") as fle:
        fle.write(our_goddamn_fucking_dictionary)


# this function sucks ass, its easier to do it yourself than tune this shit
def add_short_versions():
    with open("codes.txt", "r+") as fle:
        our_goddamn_fucking_dictionary = fle.read()
        our_goddamn_fucking_dictionary = our_goddamn_fucking_dictionary.replace("ё", "е")
        print(re.findall(r'[а-я]*(?= вокзал)', our_goddamn_fucking_dictionary))
    #
    # with open("codes.txt", "w+") as fle:
    #     fle.write(our_goddamn_fucking_dictionary)


add_short_versions()