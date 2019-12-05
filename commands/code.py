import command_system
import pymysql
from settings import user, password, host


def code(player_id, command):
    try:
        code, nickname = command.split(' ')[1], command.split(' ')[2]
    except IndexError:
        message = 'Необходимо ввести свой игровой ID и никнейм. Их можно найти в Throne Room, а также во вкладках Friends и Profile. Вводите данные через пробел в формате /код ваш_ID ваш_никнейм'
        return [message]
    if not code.isalnum() or not len(code) == 16:
        message = 'Неправильный формат ввода. Убедитесь что указан ваш игровой ID. Его можно найти в Throne Room, а также во вкладках Friends и Profile.'
        return [message]
    if not 3 <= len(nickname) <= 20:
        message = 'Неправильный формат ввода. Убедитесь что указан ваш никнейм. Его можно найти в Throne Room, а также во вкладке Profile.'
        return [message]
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT EXISTS(SELECT player_id FROM players WHERE player_id = %s)', (player_id, ))
        if cur.fetchone()[0]:
            cur.execute('UPDATE players SET code = %s, nickname = %s WHERE player_id = %s;', (code, nickname, player_id))
            message = 'Код и никнейм успешно обновлены:\nКод: {0}\nНикнейм: {1}'.format(code, nickname)
            return [message]
        else:
            cur.execute('INSERT players(player_id, code, nickname, host_elo, elo, joining_time) VALUES (%s, %s, %s, 1000, 1000, NOW());', (player_id, code, nickname))
            message = 'Вы успешно зарегистрированы в системе!\nКод: {0}\nНикнейм: {1}'.format(code, nickname)
            return [message]


code_command = command_system.Command()

code_command.keys = ['код', 'регистрация', 'code']
code_command.description = ' игровой_ID никнейм - Регистрация/обновление в системе посредством ввода своего игровго ID и никнейма.'
code_command.process = code
