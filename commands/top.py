import command_system
import pymysql
from settings import user, password, host
import message_handler
import elo


def top(player_id, command):
    space = command.find(' ')
    elo.recalculate()
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        if space == -1:
            cur.execute('SELECT player_id, host_elo, elo FROM players WHERE host_elo + elo > 2000 ORDER BY (host_elo + elo) DESC;')
            rows = cur.fetchmany(min(10, cur.rowcount))
            message = 'ТОП-10:\n\n'
            for row in rows:
                message += message_handler.username(row[0]) + ': ' + str(row[1]) + ' / ' + str(row[2]) + ' ЭЛО\n'
        elif command[space:] in (' хост', ' host'):
            cur.execute('SELECT player_id, host_elo FROM players WHERE host_elo > 1050 ORDER BY host_elo DESC;')
            rows = cur.fetchmany(min(10, cur.rowcount))
            message = 'ТОП-10 (хост):\n\n'
            for row in rows:
                message += message_handler.username(row[0]) + ': ' + str(row[1]) + ' ЭЛО\n'
        elif command[space:] in (' второй', ' away'):
            cur.execute('SELECT player_id, elo FROM players WHERE elo > 950 ORDER BY elo DESC;')
            rows = cur.fetchmany(min(10, cur.rowcount))
            message = 'ТОП-10 (второй):\n\n'
            for row in rows:
                message += message_handler.username(row[0]) + ': ' + str(row[1]) + ' ЭЛО\n'
        else:
            message = 'Неправильный формат ввода. Попробуйте просто /топ.'
            return [message]
        return [message]


top_command = command_system.Command()

top_command.keys = ['топ', 'top']
top_command.description = ' (_ / хост / второй) - Игроки с наивысшим ЭЛО-рейтингом.'
top_command.process = top
