import command_system


def tribe_selection(player_id, command):
    message = 'Ваше плямя - Люксидор - много яблок, мало гор.'
    return [message]

tribe_selection_command = command_system.Command()

tribe_selection_command.keys = ['выбор_племени', 'tribe_selection']
tribe_selection_command.description = ' - Решаете, какое племя приобрести? Эта команда для вас.'
tribe_selection_command.process = tribe_selection
