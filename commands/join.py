import command_system
import pymysql
from settings import user, password, host
import message_handler


def join(player_id, command):
    space = command.find(' ')
    if space == -1:
        message = 'Необходимо ввести ID игры в которую вы хотите войти.'
        return [message]
    game_id = command[space:]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT host_id FROM games WHERE game_id = %s AND type = \'o\' AND away_id IS NULL;', (game_id, ))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено открытых игр с указанным ID.'
            return [message]
        if fetch[0] == player_id:
            message = 'Нельзя играть с самим собой.'
            return [message]
        cur.execute('SELECT code FROM players WHERE player_id = %s;', (player_id, ))
        player = cur.fetchone()
        if not player:
            message = 'Вы не зарегистрированы в системе. Воспользуйтесь справкой: /помощь.'
            return [message]
        cur.execute('UPDATE games SET away_id = %s, type = \'r\', starting_time = NOW() WHERE game_id = %s;', (player_id, game_id))
        message = 'Вы успешно присоединились к игре {0}.\n\n[id{1}|{2}], ваша игра заполнена. Теперь вам нужно создать игру в Политопии. Не забудьте применить команду /начать с названием новой игры. ID вашего противника:'.format(str(game_id), fetch[0], message_handler.username(fetch[0]))
        return [message, player[0]]


join_command = command_system.Command()

join_command.keys = ['войти', 'зайти', 'join']
join_command.description = ' ID_игры - Войти в открытую игру. Ваш противник создаст игру в Политопии и пригласит вас в неё.'
join_command.process = join
