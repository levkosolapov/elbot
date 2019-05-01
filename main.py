import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import settings
import new


def increment_random_id():
    global i_will_never_use_global_variables_again
    i_will_never_use_global_variables_again += 1


def write_msg(user_id, message):
    random_var = i_will_never_use_global_variables_again
    vk.method('messages.send', {'user_id': user_id, 'random_id': random_var, 'message': message})
    increment_random_id()


#add_logs, add user error handling for flags
def parse_response(request, user_id):
    request = request.split()
    flag1_dict = {'сегодня': '','завтра': ''}

    if not ((request[0] == 'от' or 'с') and request[2] == 'до'):
        write_msg(user_id, 'dont feed me with shit')
        # print('dont feed me shit')

    else:
        if len(request) > 5 or len(request) < 4:
            write_msg(user_id, 'dont feed me with shit, too long request')
            # print('dont feed me with shit, too long request')
        elif len(request) == 4:
            try:
                src = request[1]
                dest = request[3]
                body = new.finally_the_fucking_message_body(src, dest)
                write_msg(user_id, body)
            except Exception as e:
                print('here i sholuld save error to logs', e)
        else:
            if request[4] not in flag1_dict.keys():
                pass



def main():

    # Основной цикл
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:

            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:

                # Сообщение от пользователя
                request = event.text

                # Каменная логика ответа
                if request == "привет":
                    write_msg(event.user_id, "Хуй соси")
                elif request == "пока":
                    # write_msg(event.user_id, "фывфывфыв")
                    messssage = """До свидания, уебище лесное.
                     Дери тебя тысяча чертей раскаленными кочергами.
                      Просто убей себя, ты сделаешь миру большую услугу - про таких как ты говорят: вроде и на человека похож, а по факту - пидарас пидарасом.
                      Помни - если я когда-нибудь встечу тебя на помойке, на которой ты живешь, 
                      я обоссу тебе ебало и сожгу твой дом.
                      Ведь ты живешь в картонной коробке, на которую ссут собаки и срут залетные птицы.
                      Падающее говно залетных птиц шлепается об твое унылое ебало каждый день, оставляя неизгладимый аромат зашкварности на твоей мелочной душонке.
                      Удачной прогулки на хуй, пидрило подзаборное, мразь подпарашная, гнида обоссаная тремя макаками, гад, сволочь, говно, жопа!!!!!"""
                    write_msg(event.user_id, messssage)
                else:
                    parse_response(request,event.user_id)


if __name__ == '__main__':
    # Авторизуемся как сообщество
    vk = vk_api.VkApi(token=settings.token)

    # Работа с сообщениями
    longpoll = VkLongPoll(vk)

    # заводим random_id - глобальную, чтобы сообщения точно не пересеклись
    i_will_never_use_global_variables_again = 30

    main()
