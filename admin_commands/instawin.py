import command_system
import pymysql
from settings import user, password, host
import message_handler


def instawin(player_id, command):
    try:
        _, winner, game_id = command.split()
    except:
        message = 'Необходимо указать победителя и ID игры в системе.'
        return [message]
    try:
        player_id = message_handler.id_by_link(winner.split('@')[1][:-1])
    except (TypeError, IndexError):
        message = 'Некорректная ссылка. Нажмите @ или * чтобы выбрать среди участников беседы.'
        return [message]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT host_id, away_id FROM games WHERE game_id = %s AND (type = \'i\' OR type = \'w\' OR type = \'c\') AND (host_id = %s OR away_id = %s);', (game_id, player_id, player_id))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено игр с указанным ID.'
            return [message]
        if player_id == fetch[0]:
            cur.execute('UPDATE games SET host_winner = 1, type = \'c\', starting_time = NOW() WHERE game_id = %s;', (game_id, ))
            cur.execute('SELECT game_id FROM results WHERE game_id = %s;', (game_id, ))
            exists = cur.fetchone()
            if exists:
                cur.execute('UPDATE results SET host_winner = 1 WHERE game_id = %s;', (game_id, ))
            else:
                cur.execute('INSERT results(host_id, away_id, host_winner, game_id) VALUES (%s, %s, %s, %s);', (fetch[0], fetch[1], 1, game_id))
            message = 'Игра {0} завершена, победитель - {1}!'.format(game_id, message_handler.username(fetch[0]))
            return [message]
        elif player_id == fetch[1]:
            cur.execute('UPDATE games SET host_winner = 0, type = \'c\', starting_time = NOW() WHERE game_id = %s;', (game_id, ))
            cur.execute('SELECT game_id FROM results WHERE game_id = %s;', (game_id, ))
            exists = cur.fetchone()
            if exists:
                cur.execute('UPDATE results SET host_winner = 0 WHERE game_id = %s;', (game_id, ))
            else:
                cur.execute('INSERT results(host_id, away_id, host_winner, game_id) VALUES (%s, %s, %s, %s);', (fetch[0], fetch[1], 0, game_id))
            message = 'Игра {0} завершена, победитель - {1}!'.format(game_id, message_handler.username(fetch[1]))
            return [message]


instawin_command = command_system.AdminCommand()

instawin_command.keys = ['instawin']
instawin_command.description = ' упоминание_игрока ID_игры - Определить победителя игры.'
instawin_command.process = instawin
