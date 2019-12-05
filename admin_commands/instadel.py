import command_system
import pymysql
from settings import user, password, host


def instadel(player_id, command):
    space = command.find(' ')
    if space == -1:
        message = 'Необходимо ввести ID игры которую нужно удалить.'
        return [message]
    game_id = command[space:]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT game_id FROM games WHERE game_id = %s;', (game_id, ))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не игр с указанным ID.'
            return [message]
        cur.execute('DELETE FROM games WHERE game_id = %s;', (game_id, ))
        message = 'Игра успешно удалена.'
        cur.execute('SELECT game_id FROM results WHERE game_id = %s;', (game_id, ))
        fetch = cur.fetchone()
        if fetch:
            cur.execute('DELETE FROM results WHERE game_id = %s;', (game_id, ))
            message += ' Также удалён результат игры.'
        return [message]


instadel_command = command_system.AdminCommand()

instadel_command.keys = ['instadel']
instadel_command.description = ' ID_игры - Удалить игру.'
instadel_command.process = instadel
