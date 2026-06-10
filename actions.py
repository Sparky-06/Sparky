import subprocess
import webbrowser
import os

from loguru import logger


# ----------------------
# SAFE EXECUTION HELPERS
# ----------------------

def safe_popen(command):
    try:
        subprocess.Popen(command)
        logger.info(f"Success : \"{command}\"successful command execution")
    except FileNotFoundError:
        print(f"Application not found: {command[0]}")
        logger.error(f"Error : \"{command}\" - Application not found")

    except Exception as e:
        print(f"Error launching application: {e}")
        logger.critical(f"Error : \"{command}\"Error lunching application")


def safe_run(command):
    try:
        subprocess.run(command, check=True)
        logger.info(f"Success : \"{command}\" Successful command execution")
    except FileNotFoundError:
        print(f"Command not found: {command[0]}")
        logger.error(f"Error : \"{command}\" Command not found")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        logger.error(f"Error : \"{command}\" Command failed")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logger.critical(f"Error : \"{command}\" Unexpected error in command execution")


def safe_web_open(url):
    try:
        webbrowser.open(url)
        logger.info(f"Success : {url} - Successful url access")
    except Exception as e:
        print(f"Failed to open website: {e}")
        logger.critical(f"Error : {url} - Failed to open website")


# ----------------------
# APPS
# ----------------------

def open_spotify():
    safe_popen(["flatpak", "run", "com.spotify.Client"])


def open_code():
    safe_popen(["code"])


def open_terminal():
    safe_popen(["gnome-terminal"])


def open_files():
    safe_popen(["nautilus"])


def open_calculator():
    safe_popen(["gnome-calculator"])


def open_settings():
    safe_popen(["gnome-control-center"])


def open_discord():
    safe_popen(["flatpak", "run", "com.discordapp.Discord"])


def open_chrome():
    safe_popen(["google-chrome"])


def open_firefox():
    safe_popen(["firefox"])


# ----------------------
# WEBSITES
# ----------------------

def open_youtube():
    safe_web_open("https://youtube.com")


def open_google():
    safe_web_open("https://google.com")


def open_gmail():
    safe_web_open("https://mail.google.com")


def open_github():
    safe_web_open("https://github.com")


def open_chatgpt():
    safe_web_open("https://chat.openai.com")


def open_vtop():
    safe_web_open("https://vtopcc.vit.ac.in/vtop/login")


def open_linkedin():
    safe_web_open("https://linkedin.com")


def open_reddit():
    safe_web_open("https://reddit.com")


def open_whatsapp():
    safe_web_open("https://web.whatsapp.com")


# ----------------------
# SYSTEM CONTROLS
# ----------------------

# Uncomment when you trust your speech recognition more than random fan noise.

# def shutdown_pc():
#     try:
#         os.system("shutdown now")
#     except Exception as e:
#         print(f"Shutdown failed: {e}")

# def restart_pc():
#     try:
#         os.system("reboot")
#     except Exception as e:
#         print(f"Restart failed: {e}")

# def lock_screen():
#     safe_run(["gnome-screensaver-command", "-l"])

# def sleep_pc():
#     safe_run(["systemctl", "suspend"])

def lock_screen():
    safe_run(["loginctl", "lock-session"])



def battery_status():
    safe_run(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"])


def wifi_on():
    safe_run(["nmcli", "radio", "wifi", "on"])

def wifi_off():
    safe_run(["nmcli", "radio", "wifi", "off"])

def wifi_toggle():
    safe_run(["nmcli", "radio", "wifi"])


def bluetooth_toggle():
    safe_run(["bluetoothctl", "power", "toggle"])




# ----------------------
# VOLUME
# ----------------------

def volume_up():
    safe_run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"])


def volume_down():
    safe_run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"])


def mute_volume():
    safe_run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])


# ----------------------
# BRIGHTNESS
# ----------------------

def brightness_up():
    safe_run(["brightnessctl", "set", "+10%"])


def brightness_down():
    safe_run(["brightnessctl", "set", "10%-"])


# ----------------------
# MEDIA
# ----------------------

def play_pause():
    safe_run(["playerctl", "play-pause"])


def next_track():
    safe_run(["playerctl", "next"])


def previous_track():
    safe_run(["playerctl", "previous"])


# ----------------------
# SEARCH
# ----------------------

def search_google(query):
    safe_web_open(f"https://www.google.com/search?q={query}")


def search_youtube(query):
    safe_web_open(f"https://www.youtube.com/results?search_query={query}")


def cricket_score():
    safe_web_open("https://www.google.com/search?q=Cricket%20Score")



