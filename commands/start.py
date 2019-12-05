import command_system
import pymysql
from settings import user, password, host
from utils import delete_mentions
import message_handler


def start(player_id, command):
    try:
        _, game_id, *args = command.split()
        if len(' '.join(args)) > 30:
            message = 'Необходимо ввести название игры в Политопии.'
            return [message]
        name = delete_mentions(' '.join(args))
    except:
        message = 'Необходимо ввести ID игры в системе и её название в Политопии.'
        return [message]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT away_id FROM games WHERE game_id = %s AND type = \'r\' AND host_id = %s;', (game_id, player_id))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено ваших ожидающих начала игр с указанным ID.'
            return [message]
        cur.execute('UPDATE games SET name = %s, type = \'i\', starting_time = NOW() WHERE game_id = %s;', (name, game_id))
        message = 'Игра {0} успешно создана.\n\n[id{1}|{2}], в ближайшее время вы будете приглашены в игру {3}.'.format(str(game_id), fetch[0], message_handler.username(fetch[0]), name)
        return [message]


start_command = command_system.Command()

start_command.keys = ['начать', 'старт', 'start']
start_command.description = ' ID_игры Название_Игры - Начать заполненную игру. Перед применением команды начните игру в Политопии и укажите здесь её название.'
start_command.process = start
