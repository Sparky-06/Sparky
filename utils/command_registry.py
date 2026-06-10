from command_modules.music_commands import music_commands
from command_modules.system_commands import system_commands
from command_modules.web_commands import web_commands

ALL_COMMANDS = {}

ALL_COMMANDS.update(music_commands)
ALL_COMMANDS.update(system_commands)
ALL_COMMANDS.update(web_commands)