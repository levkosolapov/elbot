import requests
import json
import datetime
import tools


# should change algo here in order to take closest key by the D-L distance
def make_code_from_query(s1: str):
    s1 = s1.lower()
    for i in codes_dict.keys():
        if tools.damerau_levenshtein_distance(i, s1) < 3:
            return codes_dict[i]
    # if there are no similar names, it returns none


# similar to make_code_from_query
def make_name_from_query(s1: str):
    s1 = s1.lower()
    for i in codes_dict.keys():
        if tools.damerau_levenshtein_distance(i, s1) < 3:
            return i
    # if there are no similar names, it returns none


def create_request(src,dest):
    blank = 'https://api.rasp.yandex.net/v3.0/search/?apikey=1909bac1-29ce-4bad-869b-a58c33c76078&format=json&result_timezone=Europe/Moscow&from={}&to={}&lang=ru_RU&transport_types=suburban&date={}'
    now1 = datetime.date.today().isoformat()
    req = blank.format(src, dest, now1)
    return req


def get_raspis(src, dest):
    request1 = create_request(src, dest)
    raspis = requests.get(request1)
    data = json.loads(raspis.text)
    return data

#
# def dump_raspis(data):
#     jsondata = json.dumps(data)
#     with open("request.txt", "w") as f:
#         f.write(jsondata)


def timetable_gen(data):
    now1 = datetime.datetime.now()
    for item in data['segments']:
        deptime  = item['departure'][11:len(item['departure'])-6]
        arrtime = item['arrival'][11:len(item['departure'])-6]
        depdatetime = datetime.datetime.strptime(item['departure'][0:len(item['departure'])-6].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        arrdatetime = datetime.datetime.strptime(item['arrival'][0:len(item['arrival'])-6].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        if now1 < depdatetime:
            yield deptime, arrtime


# the one and only function we call from main
def request_timetable(s1: str, s2: str):
    src = make_code_from_query(s1)
    dest = make_code_from_query(s2)
    if src and dest:
        data = get_raspis(src,dest)
        return timetable_gen(data)
    else:
        print('shits fucked, нет таких станций, мразь, писать научись, сука!!!!')


def finally_the_fucking_message_body(src, dest):
    body = make_name_from_query(src) + '\t' + make_name_from_query(dest) + '\n'
    for i in request_timetable(src, dest):
        body = body + i[0] + '\t' + i[1] + '\n'
    # print(body)
    return body

codes_dict = {'долгопрудная': 's9600766', 'новодачная': 's9601261', 'москва (курский вокзал)': 's2000001', 'москва (ярославский вокзал)': 's2000002', 'москва (казанский вокзал)': 's2000003', 'москва (павелецкий вокзал)': 's2000005', 'москва (белорусский вокзал)': 's2000006', 'москва (киевский вокзал)': 's2000007', 'москва (рижский вокзал)': 's2000008', 'москва (савёловский вокзал)': 's2000009', 'москва (ленинградский вокзал)': 's2006004', 'москва-каланчёвская': 's2001005', 'москва запасной код': 's9600676', 'битца': 's9600703', 'текстильщики': 's9600711', 'тушино': 's9600741', 'матвеевская': 's9600771', 'царицыно': 's9600891', 'дмитровская': 's9600901', 'рабочий посёлок': 's9600911', 'перово': 's9600931', 'солнечная': 's9600981', 'плющево': 's9601186', 'ржевская': 's9601266', 'сортировочная': 's9601335', 'выхино': 's9601627', 'косино': 's9601635', 'новая': 's9601642', 'электрозаводская': 's9601647', 'коломенское': 's9601656', 'кусково': 's9601671', 'бирюлёво-пасс.': 's9601703', 'новогиреево': 's9601737', 'серп и молот': 's9601796', 'карачарово': 's9601835', 'чухлинка': 's9601856', 'вешняки': 's9601964', 'фрезер': 's9601991', 'марк': 's9602214', 'нати': 's9603256', 'петровско-разумовское': 's9603458', 'моссельмаш': 's9603478', 'останкино': 's9603505', 'фили': 's9600821', 'лось': 's9600831', 'лианозово': 's9600851', 'калитники': 's9600866', 'очаково': 's9600881', 'москва-тов.-смоленская': 's9600940', 'сетунь': 's9600941', 'москва-3': 's9601018', 'белокаменная': 's9601063', 'дегунино': 's9601117', 'северянин': 's9601217', 'яуза': 's9601236', 'покровское-стрешнево': 's9601251', 'покровская': 's9601256', 'бутово': 's9601291', 'москва 2 митьково': 's9601312', 'локомотив': 's9601334', 'сколково': 's9601342', 'тестовская': 's9601349', 'савёловская': 's9601382', 'станколит': 's9601384', 'беговая': 's9601666', 'москва-сортировочная': 's9601674', 'ленинградская': 's9601688', 'бирюлёво-тов.': 's9601698', 'москворечье': 's9601711', 'лосиноостровская': 's9601716', 'кунцево': 's9601728', 'булатниково': 's9601741', 'люблино': 's9601788', 'бескудниково': 's9601805', 'москва-товарная': 's9601813', 'окружная': 's9601830', 'маленковская': 's9601882', 'перерва': 's9601898', 'гражданская': 's9601934', 'москва-тов.-рязанская': 's9601938', 'красный строитель': 's9601943', 'красный балтиец': 's9601947', 'нижние котлы': 's9601975', 'тульская (бывш. зил)': 's9601985', 'переделкино': 's9602014', 'москва-товарная': 's9602028', 'трикотажная': 's9602036', 'чертаново': 's9602125', 'депо': 's9602245', 'москва-тов.-ярославская': 's9602304', 'кунцево 2': 's9602450', 'тимирязевская': 's9602463', 'рижская': 's9603518', 'москва-тов.': 's9603857', 'ховрино': 's9603877', 'москва-инт': 's9603919', 'москва сут': 's9603926', 'канатчиково': 's9623265', 'новопеределкино': 's9799753', 'андроновка': 's9855157', 'кутузовская (мцк)': 's9855158', 'владыкино': 's9855159', 'измайлово': 's9855160', 'соколиная гора': 's9855161', 'шоссе энтузиастов': 's9855162', 'нижегородская': 's9855163', 'новохохловская (мцк)': 's9855164', 'угрешская': 's9855165', 'дубровка': 's9855166', 'автозаводская': 's9855167', 'зил (мцк)': 's9855168', 'верхние котлы (мцк)': 's9855169', 'крымская': 's9855170', 'площадь гагарина': 's9855171', 'лужники': 's9855172', 'деловой центр': 's9855173', 'шелепиха': 's9855174', 'хорошёво': 's9855175', 'зорге': 's9855176', 'панфиловская': 's9855177', 'стрешнево': 's9855178', 'балтийская': 's9855179', 'коптево': 's9855180', 'лихоборы': 's9855181', 'окружная (мцк)': 's9855182', 'ботанический сад': 's9855184', 'ростокино': 's9855186', 'бульвар рокоссовского': 's9855187', 'улица сергея эйзенштейна': 's9859403', 'выставочный центр': 's9859404', 'улица академика королёва': 's9859405', 'телецентр': 's9859406', 'улица милашенкова': 's9859407', 'тимирязевская (монорельс)': 's9859408', 'новохохловская': 's9868807', 'верхние котлы': 's9868808', 'москва': 's9600674' }

# data = get_raspis(src,dest)
# dump_raspis(data)
# for items in data['segments']:
#     print(item)
# print(data)
#
# with open('request.txt', 'r') as f:
#     data = json.loads(f.read())
# for i in timetable_gen(data):
#     print(i[0], i[1])
#
# for i in timetable_gen(data):
#     print(i[0], i[1])
#
# s1 = input()
# s2 = input()
# try:
#     for i in request_timetable(s1,s2):
#         print(i[0], i[1])
# except Exception as e:
#     print(e)
#
# finally_the_fucking_message_body(s1,s2)