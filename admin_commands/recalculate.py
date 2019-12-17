import command_system
import elo


def recalculate(player_id, command):
    elo.recalculate()
    message = 'Рейтинг обновлён.'
    return [message]


recalculate_command = command_system.AdminCommand()

recalculate_command.keys = ['recalculate']
recalculate_command.description = ' - Перерасчёт рейтинга.'
recalculate_command.process = recalculate
