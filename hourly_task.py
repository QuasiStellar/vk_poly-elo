import pymysql
from settings import user, password, host, bot_commands, token
import message_handler


connection = pymysql.connect(host, user, password, user + '$main')
with connection:
    cur = connection.cursor()
    cur.execute('SELECT game_id, host_id, away_id, host_winner FROM games WHERE type = \'w\' AND TIMESTAMPDIFF(HOUR, starting_time, NOW()) >= 24;')
    rows = cur.fetchall()
    message = ''
    for row in rows:
        cur.execute('UPDATE games SET type = \'c\' WHERE game_id = %s;', (row[0], ))
        cur.execute('INSERT results(host_id, away_id, host_winner, game_id) VALUES (%s, %s, %s, %s);', (row[1], row[2], row[3], row[0]))
        message += 'Игра №{0} завершена в соответствии с заявлением победителя ([id{1}|{2}]).\n\n'.format(row[0], row[1] if row[3] else row[2], message_handler.username(row[1] if row[3] else row[2]))
    if message:
        message_handler.send_message_chat(bot_commands, token, message)
