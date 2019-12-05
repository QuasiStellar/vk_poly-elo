import command_system
import pymysql
from settings import user, password, host


def delete(player_id, command):
    space = command.find(' ')
    if space == -1:
        message = 'Необходимо ввести ID игры которую нужно удалить.'
        return [message]
    game_id = command[space:]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT game_id FROM games WHERE game_id = %s AND (type = \'o\' OR type = \'r\') AND host_id = %s;', (game_id, player_id))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено открытых или готовых к старту игр с указанным ID.'
            return [message]
        cur.execute('DELETE FROM games WHERE game_id = %s;', (game_id, ))
        message = 'Игра успешно удалена.'
        return [message]


delete_command = command_system.Command()

delete_command.keys = ['удалить', 'delete']
delete_command.description = ' ID_игры - Исключить противника из вашей ещё не стартовавшей игры.'
delete_command.process = delete
