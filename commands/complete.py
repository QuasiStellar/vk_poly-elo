import command_system
import pymysql
from settings import user, password, host
import message_handler


def complete(player_id, command):
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        page = 1
        try:
            page = int(command.split(' ')[1])
        except (ValueError, IndexError):
            message = 'Укажите страницу результатов.'
            return [message]
        self = True
        try:
            pointer = command.split(' ')[2]
            try:
                player_id = message_handler.id_by_link(pointer.split('@')[1][:-1])
                self = False
            except (TypeError, IndexError):
                message = 'Некорректная ссылка. Нажмите @ или * чтобы выбрать среди участников беседы.'
                return [message]
        except IndexError:
            pass
        message = 'Завершённые игры с вашим участием:\n\n' if self else 'Завершённые игры с участием игрока:\n\n'
        cur.execute('SELECT game_id, name, host_id, away_id, description, host_winner FROM games WHERE type = \'c\' AND (host_id = %s OR away_id = %s) ORDER BY starting_time DESC;', (player_id, player_id))
        rows = cur.fetchall()
        if rows:
            count = 0
            for row in rows:
                if count // 10 + 1 == page:
                    result = 'ПОБЕДА' if row[5] == (player_id == row[2]) else 'ПОРАЖЕНИЕ'
                    message += str(row[0]) + ' - ' + str(row[1]) + '\n' + message_handler.username(row[2]) + ' vs ' + message_handler.username(row[3]) + '\n' + str(row[4]) + '\n' + result + '\n\n'
                count += 1
        return [message]


complete_command = command_system.Command()

complete_command.keys = ['завершённые', 'complete']
complete_command.description = ' номер страницы игр (по 10 на странице) [упоминание игрока] - Завершённые игры.'
complete_command.process = complete