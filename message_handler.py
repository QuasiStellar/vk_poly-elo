import vk
import os
import importlib
from command_system import command_list, admin_command_list
import pymysql
from settings import user, password, host, token, admin_id, project_folder


session = vk.Session()
api = vk.API(session, v=5.0)


def load_modules():
    files = os.listdir(project_folder + "/commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        spec = importlib.util.spec_from_file_location(m, project_folder + "/commands/" + m)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
    files = os.listdir(project_folder + "/admin_commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        spec = importlib.util.spec_from_file_location(m, project_folder + "/admin_commands/" + m)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)


def get_answer(u, command):
    args = ["Команда не распознана. Напишите '/помощь', чтобы получить список команд."]
    for c in command_list:
        if command[1:].lower().split(' ')[0] in c.keys:
            args = c.process(u, command)
    return args


def get_admin_answer(u, command):
    args = []
    for c in admin_command_list:
        if command[1:].lower().split(' ')[0] in c.keys:
            if u != admin_id:
                args = ["Отказано в доступе."]
                return args
            args = c.process(u, command)
    return args


def create_message_chat(token, u, chat, command, prefix):
    connection = pymysql.connect(host, user, password, user + '$main')
    cur = connection.cursor()
    cur.execute('SELECT EXISTS(SELECT player_id FROM players WHERE player_id = %s AND role = \'Banned\')', (u, ))
    if cur.fetchone()[0]:
        send_message_chat(chat, token, 'С лёгким паром!')
        return
    args = get_answer(u, command) if prefix == '/' else get_admin_answer(u, command)
    for arg in args:
        send_message_chat(chat, token, arg)


def create_message(token, u, command, prefix):
    connection = pymysql.connect(host, user, password, user + '$main')
    cur = connection.cursor()
    cur.execute('SELECT EXISTS(SELECT player_id FROM players WHERE player_id = %s AND role = \'Banned\')', (u, ))
    if cur.fetchone()[0]:
        send_message(u, token, 'С лёгким паром!')
        return
    args = get_answer(u, command) if prefix == '/' else get_admin_answer(u, command)
    for arg in args:
        send_message(u, token, arg)


def send_message_chat(chat_id, token, message):
    api.messages.send(access_token=token, chat_id=str(chat_id), message=message)


def send_message(user_id, token, message):
    api.messages.send(access_token=token, user_id=str(user_id), message=message)


def username(user_id):
    info = api.users.get(access_token=token, user_ids = [user_id])
    return info[0]['first_name'] + ' ' + info[0]['last_name']


def id_by_link(link):
    info = api.utils.resolveScreenName(access_token=token, screen_name=link)
    return info['object_id']
