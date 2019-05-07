import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import settings
import new
import tools
import datetime


def increment_random_id():
    global i_will_never_use_global_variables_again
    i_will_never_use_global_variables_again += 1


def write_msg(user_id, message):
    random_var = i_will_never_use_global_variables_again
    vk.method('messages.send', {'user_id': user_id, 'random_id': random_var, 'message': message})
    increment_random_id()


def main():

    # Основной цикл
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:

            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:

                # Сообщение от пользователя
                request = event.text
                if any(c in request for c in ['привет', 'здравствуйте', 'help', 'начать', 'start']):
                    write_msg(event.user_id, '''напишите ваш запрос в виде "от ... до ... ".
                     Также можете приписать в конце "завтра" или день недели''')
                elif any(c in request for c in ['жопа', 'хуй', 'говно', 'пошел', 'нахуй', 'пидор', 'сука', 'пидор', 'ублюдок', 'мать', 'твою', 'блядь', 'жлоб', 'скотина']):
                    write_msg(event.user_id, 'ты чего, ругаться на меня вздумал? А ну быстро извинись')
                elif ('извини' or 'прости' or 'извините' or 'извиняюсь' or 'извинения') in request:
                    write_msg(event.user_id, 'извинения приняты')
                    write_msg(event.user_id, '''напишите ваш запрос в виде "от ... до ... ".
                    Также можете приписать в конце "завтра" или день недели''')
                else:
                    if len(request) < 4:
                        write_msg(event.user_id, 'ерунду какую-то написал и радуешься. Пиши так, например: "от А до В завтра"')
                    else:
                        try:
                            (source, dest, zeitpunkt) = tools.unstable_parser(request)
                            body = new.finally_the_fucking_message_body(source, dest, zeitpunkt)
                            write_msg(event.user_id, body)
                        # TODO: exception handling+ logs
                        except Exception as e:
                            print(e)
                            pass


if __name__ == '__main__':
    # Авторизуемся как сообщество
    vk = vk_api.VkApi(token=settings.token)

    # Работа с сообщениями
    longpoll = VkLongPoll(vk)

    # заводим random_id - глобальную, чтобы сообщения точно не пересеклись
    i_will_never_use_global_variables_again = 67

    main()
