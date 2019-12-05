import command_system
import pymysql
from settings import user, password, host
import message_handler


def ban(player_id, command):
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        pointer = command.split(' ')[1]
        if len(pointer) > 1 and pointer[0] == '[' and pointer[-1] == ']' and not pointer[-2] == '@':
            try:
                player_id = message_handler.id_by_link(pointer.split('@')[1][:-1])
            except (TypeError, IndexError):
                message = 'Некорректная ссылка. Нажмите @ или * чтобы выбрать среди участников беседы.'
                return [message]
            cur.execute('SELECT EXISTS(SELECT player_id FROM players WHERE player_id = %s)', (player_id, ))
            if cur.fetchone()[0]:
                cur.execute('UPDATE players SET role = \'Banned\', nickname = \'deleted\', code \'0000000000000000\' WHERE player_id = %s', (player_id, ))
            else:
                message = 'Этот пользователь ещё не зарегистрирован в системе.'
                return [message]
        else:
            message = 'Некорректная ссылка. Нажмите @ или * чтобы выбрать среди участников беседы.'
            return [message]
        message = 'Пользователь забанен.'
        return [message]


ban_command = command_system.AdminCommand()

ban_command.keys = ['ban']
ban_command.description = ' упоминание - Бан пользователя в системе.'
ban_command.process = ban
