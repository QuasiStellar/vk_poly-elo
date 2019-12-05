import command_system
import pymysql
from settings import user, password, host
import message_handler
import elo


def games(player_id, command):
    elo.recalculate()
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT game_id, host_id, description FROM games WHERE type = \'o\' ORDER BY starting_time ASC;')
        rows = cur.fetchmany(min(10, cur.rowcount))
        message = 'Открытые игры:\n\n'
        for row in rows:
            cur.execute('SELECT host_elo FROM players WHERE player_id = %s;', (row[1], ))
            rating = cur.fetchone()[0]
            message += 'ID: ' + str(row[0]) + ' - ' + message_handler.username(row[1]) + ' - ' + str(rating) + ' ELO\n' + row[2] + '\n\n'
        return [message]


games_command = command_system.Command()

games_command.keys = ['игры', 'games']
games_command.description = ' - Игры к которым можно присоединиться'
games_command.process = games