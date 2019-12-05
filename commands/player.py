import command_system
import pymysql
from settings import user, password, host
import message_handler
import elo


def player(player_id, command):
    elo.recalculate()
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        try:
            pointer = command.split(' ')[1]
        except IndexError:
            cur.execute('SELECT EXISTS(SELECT player_id FROM players WHERE player_id = %s)', (player_id, ))
            if cur.fetchone()[0]:
                cur.execute('SELECT player_id, code, nickname, host_elo, elo, joining_time, role FROM players WHERE player_id = %s', (player_id, ))
                data = cur.fetchone()
                message = '{0} - {1}\nЭЛО: {2} : {3}\nID: {4}\nНикнейм: {5}\nДата регистрации: {6}'.format(message_handler.username(data[0]), data[6] if data[6] else '', data[3], data[4], data[1], data[2], data[5])
                return [message]
            else:
                message = 'Вы ещё не зарегистрированы в системе.'
                return [message]
        if len(pointer) > 1 and pointer[0] == '[' and pointer[-1] == ']' and not pointer[-2] == '@':
            try:
                player_id = message_handler.id_by_link(pointer.split('@')[1][:-1])
            except (TypeError, IndexError):
                message = 'Некорректная ссылка. Нажмите @ или * чтобы выбрать среди участников беседы.'
                return [message]
            cur.execute('SELECT EXISTS(SELECT player_id FROM players WHERE player_id = %s)', (player_id, ))
            if cur.fetchone()[0]:
                cur.execute('SELECT player_id, code, nickname, host_elo, elo, joining_time, role FROM players WHERE player_id = %s', (player_id, ))
            else:
                message = 'Этот пользователь ещё не зарегистрирован в системе.'
                return [message]
        else:
            cur.execute('SELECT EXISTS(SELECT nickname FROM players WHERE nickname = %s)', (pointer, ))
            if cur.fetchone()[0]:
                cur.execute('SELECT player_id, code, nickname, host_elo, elo, joining_time, role FROM players WHERE nickname = %s', (pointer, ))
            else:
                message = 'Этот никнейм ещё не зарегистрирован в системе.'
                return [message]
        data = cur.fetchone()
        message = '{0} - {1}\nЭЛО: {2} : {3}\nID: {4}\nНикнейм: {5}\nДата регистрации: {6}'.format(message_handler.username(data[0]), data[6] if data[6] else '', data[3], data[4], data[1], data[2], data[5])
        return [message]


player_command = command_system.Command()

player_command.keys = ['игрок', 'player']
player_command.description = ' никнейм_игрока (или ссылка на его профиль в формате @ссылка) - Подробная информация об игроке.'
player_command.process = player
