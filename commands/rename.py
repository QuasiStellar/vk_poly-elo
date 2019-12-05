import command_system
import pymysql
from settings import user, password, host
import message_handler


def rename(player_id, command):
    try:
        _, game_id, *args = command.split()
        if len(' '.join(args)) > 30:
            message = 'Необходимо ввести название игры в Политопии.'
            return [message]
        name = ' '.join(args)
    except:
        message = 'Необходимо ввести ID игры в системе и её новое название в Политопии.'
        return [message]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT name, away_id FROM games WHERE game_id = %s AND type = \'i\' AND host_id = %s;', (game_id, player_id))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено ваших идущих игр с указанным ID.'
            return [message]
        cur.execute('UPDATE games SET name = %s, starting_time = NOW() WHERE game_id = %s;', (name, game_id))
        message = 'Игра {0} успешно переименована.\n\n[id{1}|{2}], в ближайшее время вы будете приглашены в игру {3}, из старой игры ({4}) можно выйти.'.format(str(game_id), fetch[1], message_handler.username(fetch[1]), name, fetch[0])
        return [message]


rename_command = command_system.Command()

rename_command.keys = ['переименовать', 'rename']
rename_command.description = ' ID_игры Название_Игры - Переименовать идущую игру. Использовать после каждого рестарта.'
rename_command.process = rename
