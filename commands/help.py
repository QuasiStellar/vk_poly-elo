import command_system


def help(player_id, command):
    message = 'Список команд:\n\n'
    for c in command_system.command_list:
        if not c.keys[0] == help_command.keys[0]:
            message += '/' + c.keys[0] + c.description + '\n'
    return [message]


help_command = command_system.Command()

help_command.keys = ['помощь', 'help']
help_command.process = help
