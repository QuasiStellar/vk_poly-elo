import command_system
import pymysql
from settings import user, password, host
import message_handler


me = ('я', 'me')
opponent = ('противник', 'соперник', 'враг', 'оппонент', 'opponent', 'enemy')


def win(player_id, command):
    try:
        _, winner, game_id = command.split()
        if winner not in me and winner not in opponent:
            message = 'Необходимо указать победителя (я/противник).'
            return [message]
    except:
        message = 'Необходимо указать победителя (я/противник) и ID игры в системе.'
        return [message]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT host_id, away_id FROM games WHERE game_id = %s AND (type = \'i\' OR type = \'w\') AND (host_id = %s OR away_id = %s);', (game_id, player_id, player_id))
        fetch = cur.fetchone()
        if not fetch:
            message = 'Не найдено незаконченных игр с указанным ID.'
            return [message]
        if player_id == fetch[0]:
            if winner in me:
                cur.execute('UPDATE games SET host_winner = 1, type = \'w\', starting_time = NOW() WHERE game_id = %s;', (game_id, ))
                message = 'Игра {0} завершена, победитель - {1}!\n\n[id{2}|{3}], подтвердите победу вашего противника командой /победил противник {0}. Если вы не согласны с его заявлением, обратитесь к модератору.'.format(game_id, message_handler.username(fetch[0]), fetch[1], message_handler.username(fetch[1]))
                return [message]
            else:
                cur.execute('UPDATE games SET host_winner = 0, type = \'c\', starting_time = NOW() WHERE game_id = %s;', (game_id, ))
                cur.execute('INSERT results(host_id, away_id, host_winner, game_id) VALUES (%s, %s, %s, %s);', (fetch[0], fetch[1], 0, game_id))
                message = 'Игра {0} завершена, победитель - {1}!'.format(game_id, message_handler.username(fetch[1]))
                return [message]
        elif player_id == fetch[1]:
            if winner in me:
                cur.execute('UPDATE games SET host_winner = 0, type = \'w\', starting_time = NOW() WHERE game_id = %s;', (game_id, ))
                message = 'Игра {0} завершена, победитель - {1}!\n\n[id{2}|{3}], подтвердите победу вашего противника командой /победил противник {0}. Если вы не согласны с его заявлением, обратитесь к модератору.'.format(game_id, message_handler.username(fetch[1]), fetch[0], message_handler.username(fetch[0]))
                return [message]
            else:
                cur.execute('UPDATE games SET host_winner = 1, type = \'c\', starting_time = NOW() WHERE game_id = %s;', (game_id, ))
                cur.execute('INSERT results(host_id, away_id, host_winner, game_id) VALUES (%s, %s, %s, %s);', (fetch[0], fetch[1], 1, game_id))
                message = 'Игра {0} завершена, победитель - {1}!'.format(game_id, message_handler.username(fetch[0]))
                return [message]
        else:
            message = 'Вы не участвуете в данной игре.'
            return message


win_command = command_system.Command()

win_command.keys = ['победа', 'победил', 'win']
win_command.description = ' я/противник ID_игры - Объявить о победе в игре. При сообщении о своей победе придётся дождаться подтверждения противника или подождать сутки.'
win_command.process = win
