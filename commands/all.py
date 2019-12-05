import command_system
import pymysql
from settings import user, password, host
import message_handler


def _all(player_id, command):
    space = command.find(' ')
    if space == -1:
        message = 'Необходимо ввести номер страницы которую вы хотите посмотреть.'
        return [message]
    try:
        page = int(command[space:])
    except ValueError:
        message = 'Необходимо ввести номер страницы которую вы хотите посмотреть.'
        return [message]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        message = 'Все игры в системе:\n\n'
        cur = connection.cursor()
        cur.execute('SELECT game_id, name, host_id, away_id, description, host_winner, type FROM games ORDER BY game_id DESC;')
        rows = cur.fetchall()
        if rows:
            count = 0
            for row in rows:
                if count // 10 + 1 == page:
                    if str(row[6]) == 'o':
                        message += 'ID: ' + str(row[0]) + '\n' + message_handler.username(row[2]) + ' vs ___\n' + str(row[4]) + '\n\n'
                    elif str(row[6]) == 'r':
                        message += 'ID: ' + str(row[0]) + ' - ' + str(row[1]) + '\n' + message_handler.username(row[2]) + ' vs ' + message_handler.username(row[3]) + '\n' + str(row[4]) + '\nОжидает начала.' + '\n\n'
                    elif str(row[6]) == 'i':
                        message += 'ID: ' + str(row[0]) + ' - ' + str(row[1]) + '\n' + message_handler.username(row[2]) + ' vs ' + message_handler.username(row[3]) + '\n' + str(row[4]) + '\nВ процессе.' + '\n\n'
                    elif str(row[6]) == 'w':
                        message += 'ID: ' + str(row[0]) + ' - ' + str(row[1]) + '\n' + message_handler.username(row[2]) + ' vs ' + message_handler.username(row[3]) + '\n' + str(row[4]) + '\nПобедитель: ' + message_handler.username(row[3-row[5]]) + '\nОжидает подтверждения.' + '\n\n'
                    elif str(row[6]) == 'c':
                        message += 'ID: ' + str(row[0]) + ' - ' + str(row[1]) + '\n' + message_handler.username(row[2]) + ' vs ' + message_handler.username(row[3]) + '\n' + str(row[4]) + '\nПобедитель: ' + message_handler.username(row[3-row[5]]) + '\n\n'
                count += 1
        return [message]


_all_command = command_system.Command()

_all_command.keys = ['все', 'all']
_all_command.description = ' номер_страницы - Список всех игр в системе.'
_all_command.process = _all
