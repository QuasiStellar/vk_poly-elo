import command_system
import pymysql
from settings import user, password, host
import message_handler


def incomplete(player_id, command):
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        message = ''
        anything = False
        self = True
        try:
            pointer = command.split(' ')[1]
            try:
                player_id = message_handler.id_by_link(pointer.split('@')[1][:-1])
                self = False
            except (TypeError, IndexError):
                message = 'Некорректная ссылка. Нажмите @ или * чтобы выбрать среди участников беседы.'
                return [message]
        except IndexError:
            pass
        cur = connection.cursor()
        cur.execute('SELECT game_id, host_id, away_id, description FROM games WHERE type = \'r\' AND host_id = %s ORDER BY starting_time ASC;', (player_id, ))
        rows = cur.fetchall()
        if rows:
            message += 'Вам необходимо начать следующие игры:\n\n' if self else 'Игроку необходимо начать следующие игры:\n\n'
            anything = True
            for row in rows:
                message += str(row[0]) + ' - ' + message_handler.username(row[1]) + ' vs ' + message_handler.username(row[2]) + '\n' + row[3] + '\n\n'
        cur.execute('SELECT game_id, host_id, away_id, description FROM games WHERE type = \'r\' AND away_id = %s ORDER BY starting_time ASC;', (player_id, ))
        rows = cur.fetchall()
        if rows:
            message += 'Ждём начала игры противником:\n\n'
            anything = True
            for row in rows:
                message += str(row[0]) + ' - ' + message_handler.username(row[1]) + ' vs ' + message_handler.username(row[2]) + '\n' + row[3] + '\n\n'
        cur.execute('SELECT game_id, description FROM games WHERE type = \'o\' AND host_id = %s ORDER BY starting_time ASC;', (player_id, ))
        rows = cur.fetchall()
        if rows:
            message += 'Открытые вами игры:\n\n' if self else 'Открытые игроком игры:\n\n'
            anything = True
            for row in rows:
                message += str(row[0]) + ' - ' + message_handler.username(player_id) + ' vs ___\n' + row[1] + '\n\n'
        cur.execute('SELECT game_id, host_id, away_id, description, name FROM games WHERE type = \'i\' AND (host_id = %s OR away_id = %s) ORDER BY starting_time DESC;', (player_id, player_id))
        rows = cur.fetchall()
        if rows:
            message += 'Текущие игры с вашим участием:\n\n' if self else 'Текущие игры с участием игрока:\n\n'
            anything = True
            for row in rows:
                opponent = row[1] if player_id == row[2] else row[2]
                cur.execute('SELECT code, nickname FROM players WHERE player_id = %s', (opponent, ))
                opp = cur.fetchone()
                message += str(row[0]) + ' - ' + str(row[4]) + '\n' + message_handler.username(row[1]) + ' vs ' + message_handler.username(row[2]) + '\n' + row[3] + '\nПротивник: ' + opp[1] + ' (' + opp[0] + ') ' + '\n\n'
        if not anything:
            message += 'Не найдено текущих игр.'
        return [message]


incomplete_command = command_system.Command()

incomplete_command.keys = ['текущие', 'incomplete']
incomplete_command.description = ' [упоминание игрока] - Незавершённые игры.'
incomplete_command.process = incomplete