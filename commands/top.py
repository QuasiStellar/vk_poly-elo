import command_system
import pymysql
from settings import user, password, host
import message_handler
import elo


def top(player_id, command):
    elo.recalculate()
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT player_id, host_elo, elo FROM players WHERE host_elo + elo > 2000 ORDER BY (host_elo + elo) DESC;')
        rows = cur.fetchmany(min(10, cur.rowcount))
        message = 'ТОП-10:\n\n'
        for row in rows:
            message += message_handler.username(row[0]) + ': ' + str(row[1]) + ' / ' + str(row[2]) + ' ЭЛО\n'
        return [message]

top_command = command_system.Command()

top_command.keys = ['топ', 'top']
top_command.description = ' - Игроки с наивысшим ЭЛО-рейтингом.'
top_command.process = top
