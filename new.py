import requests
import json
import datetime
import tools
from dateutil import  parser



class StNameError(Exception):
    message = ''

    def __init__(self, message):
        super().__init__('Кажется, пользователь - ебанат. Даже название станции ввести не может. Вот что он написал: '+message)


def make_code_from_query(s1: str):
    """
    this function searches for the station name, which is the closest to given by relative d-l distance.
    Raises exception if the closest station name is not close enough

    :param s1: given station name
    :return: station code
    """
    s1 = s1.lower()
    fst_key = next(iter(tools.codes_dict.keys()))
    current_distance = tools.relative_d_l_distance(fst_key,s1)
    current_value = None
    current_i = None
    for i in tools.codes_dict.keys():
        if tools.relative_d_l_distance(i, s1) < current_distance:
            # return tools.codes_dict[i]
            current_value = tools.codes_dict[i]
            current_distance = tools.relative_d_l_distance(i, s1)
            current_i = i
            print(current_value, current_distance, current_i)
    if current_distance < 0.35:
        return current_value
    else:
        raise StNameError(s1)


def make_name_from_query(s1: str):
    """
    similar to name_code_from_query, but returns station name

    :param s1:
    :return: station name
    """
    s1 = s1.lower()
    fst_key = next(iter(tools.codes_dict.keys()))
    current_distance = tools.relative_d_l_distance(fst_key,s1)
    current_value = None
    current_i = None
    for i in tools.codes_dict.keys():
        if tools.relative_d_l_distance(i, s1) < current_distance:
            # return tools.codes_dict[i]
            current_value = tools.codes_dict[i]
            current_distance = tools.relative_d_l_distance(i, s1)
            current_i = i
            print(current_value, current_distance, current_i)
    if current_distance < 0.35:
        return current_i
    else:
        raise StNameError(s1)


def get_raspis(src, dest, zeitpunkt):
    '''
    :param src: station codes
    :param dest: station codes
    :param zeitpunkt: datetime in ISO 8601 format
    :return: data from api in json format
    '''

    blank = 'https://api.rasp.yandex.net/v3.0/search/?apikey=1909bac1-29ce-4bad-869b-a58c33c76078&format=json&result_timezone=Europe/Moscow&from={}&to={}&lang=ru_RU&transport_types=suburban&date={}'
    request1 = blank.format(src, dest, zeitpunkt)
    raspis = requests.get(request1)
    data = json.loads(raspis.text)
    return data



# TODO: change time filter
def timetable_gen(data):
    now1 = datetime.datetime.now()
    for item in data['segments']:
        deptime  = item['departure'][11:len(item['departure'])-6]
        arrtime = item['arrival'][11:len(item['departure'])-6]
        depdatetime = datetime.datetime.strptime(item['departure'][0:len(item['departure'])-6].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        if now1 < depdatetime:
            yield deptime, arrtime


# the one and only function we call from main
def request_timetable(s1: str, s2: str, zeitpunkt: str):
    src = make_code_from_query(s1)
    dest = make_code_from_query(s2)
    if src and dest:
        data = get_raspis(src, dest, zeitpunkt)
        return timetable_gen(data)
    else:
        print('нет таких станций')


def howlong(t1,t2):
    t1 = parser.parse(t1)
    t2 = parser.parse(t2)
    dt = str(t2 - t1)
    araray = dt.split(':')
    if araray[0] == '0':
        result = araray[1]+' мин.'
        return result
    else:
        result = araray[0] + ' ч. '+ araray[1]+ ' мин.'
        return result

# TODO: оттестить время поездки
# TODO: обработать случай, когда поезда не идут между двумя станциями
# raise exception if there are no such stations
def finally_the_fucking_message_body(src, dest, zeitpunkt):
    '''

    :param src: src station name string. May contain user input typos
    :param dest: dest station name in string. May contain user input typos
    :param zeitpunkt: iso8601-formatted date
    :return: message body as string
    '''

    body = make_name_from_query(src) + '\t' + make_name_from_query(dest) + '\t' + zeitpunkt + '\n'
    for i in request_timetable(src, dest, zeitpunkt):
        body = body + i[0] + '\t' + i[1] + '\t'+ howlong(i[0], i[1])+'\n'
    # print(body)
    return body


# s1 = input()
# s2 = input()
# try:
#     for i in request_timetable(s1,s2):
#         print(i[0], i[1])
# except Exception as e:
#     print(e)
#
# finally_the_fucking_message_body(s1,s2)