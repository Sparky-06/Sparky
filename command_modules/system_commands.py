from actions import *

system_commands = {
    "terminal": open_terminal,
    "open terminal": open_terminal,

    "files": open_files,
    "file manager": open_files,

    "battery": battery_status,

    "wifi": wifi_toggle,
    "turn on wifi": wifi_on,
    "turn off wifi": wifi_off,

    "bluetooth": bluetooth_toggle,

#    "shutdown": shutdown_pc,
#    "restart": restart_pc,
    "lock screen": lock_screen,

    "volume up": volume_up,
    "volume down": volume_down,

    "brightness up": brightness_up,
    "brightness down": brightness_down,
}