import pymysql
from settings import user, password, host


def recalculate():
    connection = pymysql.connect(host, user, password, user + '$main')
    with connection:
        cur = connection.cursor()
        cur.execute('UPDATE players SET host_elo = 1050, elo = 950')
        cur.execute('SELECT host_id, away_id, host_winner FROM results')
        rows = cur.fetchall()
        for row in rows:
            cur.execute('SELECT host_elo FROM players WHERE player_id = %s', (row[0], ))
            elo_a = cur.fetchone()[0]
            cur.execute('SELECT elo FROM players WHERE player_id = %s', (row[1], ))
            elo_b = cur.fetchone()[0]
            new = new_rating(elo_a, elo_b, row[2])
            cur.execute('UPDATE players SET host_elo = %s WHERE player_id = %s', (new[0], row[0]))
            cur.execute('UPDATE players SET elo = %s WHERE player_id = %s', (new[1], row[1]))


def new_rating(a, b, result):
    ea = 1 / (1 + 10**((b - a) / 400))
    eb = 1 / (1 + 10**((a - b) / 400))
    new_a = a + 50 * ((1 if result else 0) - ea)
    new_b = b + 50 * ((0 if result else 1) - eb)
    return new_a, new_b
