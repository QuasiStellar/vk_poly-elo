import command_system
import pymysql
from settings import user, password, host
import message_handler


def game(player_id, command):
    space = command.find(' ')
    if space == -1:
        message = 'Необходимо ввести ID игры.'
        return [message]
    game_id = command[space:]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT type, host_id, away_id, description, starting_time, host_winner, name FROM games WHERE game_id = %s;', (game_id, ))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено игр с указанным ID.'
            return [message]
        if fetch[0] == 'o':
            message = 'Игра №{0}.\nХост: {1}\nОписание: {2}\nИгра открыта, к ней можно присоединиться командой /войти {0}'.format(str(game_id), message_handler.username(fetch[1]), fetch[3])
        if fetch[0] == 'r':
            message = 'Игра №{0}.\n{1} vs {3}\nОписание: {4}\nИгра ждёт своего начала. [id{2}|{1}], начните игру.'.format(str(game_id), message_handler.username(fetch[1]), fetch[1], message_handler.username(fetch[2]), fetch[3])
        if fetch[0] == 'i':
            message = 'Игра №{0} - {4}.\n{1} vs {2}\nОписание: {3}\nИгра в процессе.'.format(str(game_id), message_handler.username(fetch[1]), message_handler.username(fetch[2]), fetch[3], fetch[6])
        if fetch[0] == 'w':
            if fetch[5]:
                message = 'Игра №{0} - {5}.\n{1} vs {2}\nОписание: {4}\n{1} объявлен победителем. [id{3}|{2}], подтвердите победу противника командой /победил противник {0}'.format(str(game_id), message_handler.username(fetch[1]), message_handler.username(fetch[2]), fetch[2], fetch[3], fetch[6])
            else:
                message = 'Игра №{0} - {5}.\n{1} vs {2}\nОписание: {4}\n{2} объявлен победителем. [id{3}|{1}], подтвердите победу противника командой /победил противник {0}'.format(str(game_id), message_handler.username(fetch[1]), message_handler.username(fetch[2]), fetch[1], fetch[3], fetch[6])
        if fetch[0] == 'c':
            if fetch[5]:
                message = 'Игра №{0} - {4}.\n{1} vs {2}\nОписание: {3}\nПобедитель: {1}'.format(str(game_id), message_handler.username(fetch[1]), message_handler.username(fetch[2]), fetch[3], fetch[6])
            else:
                message = 'Игра №{0} - {4}.\n{1} vs {2}\nОписание: {3}\nПобедитель: {2}'.format(str(game_id), message_handler.username(fetch[1]), message_handler.username(fetch[2]), fetch[3], fetch[6])
        return [message]


game_command = command_system.Command()

game_command.keys = ['игра', 'game']
game_command.description = ' ID_игры - Посмотреть информацию об игре.'
game_command.process = game
