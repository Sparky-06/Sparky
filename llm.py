import json
import requests
import asyncio

from pydantic import BaseModel, ValidationError

import loguru as logger

from voice import speak

from memory.history import add_memory, get_memory

from memory.context import get_context, update_context

from actions import *




# =========================
# YOUR FUNCTIONS
# =========================

# import these from your actions.py

# open_spotify()
# open_code()
# open_terminal()
# open_files()
# open_calculator()
# open_settings()
# open_discord()
# open_chrome()
# open_firefox()

# open_youtube()
# open_google()
# open_gmail()
# open_github()
# open_chatgpt()
# open_vtop()
# open_linkedin()
# open_reddit()
# open_whatsapp()

# lock_screen()
# battery_status()

# wifi_on()
# wifi_off()
# wifi_toggle()

# bluetooth_toggle()

# volume_up()
# volume_down()
# mute_volume()

# brightness_up()
# brightness_down()

# play_pause()
# next_track()
# previous_track()

# search_google(query)
# search_youtube(query)

# cricket_score()


# =========================
# APP MAP
# =========================

APPS = {
    "spotify": open_spotify,
    "vscode": open_code,
    "code": open_code,
    "terminal": open_terminal,
    "files": open_files,
    "calculator": open_calculator,
    "settings": open_settings,
    "discord": open_discord,
    "chrome": open_chrome,
    "firefox": open_firefox,
}

WEBSITES = {
    "youtube": open_youtube,
    "google": open_google,
    "gmail": open_gmail,
    "github": open_github,
    "chatgpt": open_chatgpt,
    "vtop": open_vtop,
    "linkedin": open_linkedin,
    "reddit": open_reddit,
    "whatsapp": open_whatsapp,
}



# =========================
# PROMPT
# =========================

SYSTEM_PROMPT = """
You are Sparky, a Fedora Linux desktop assistant.

Your job is to:

1. Understand the user's request.
2. Decide which actions should be executed.
3. Generate a short spoken response.
4. Update memory when useful information is discovered.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use code fences.
Do NOT explain your reasoning.
Do NOT output anything except valid JSON.

You will receive:

- Conversation History
- Current Context
- User Request

Use them to understand references such as:

"open it"
"search for that"
"play something else"
"make it louder"

JSON FORMAT

{
  "intent": "<intent_name>",
  "confidence": 0.0,
  "actions": [],
  "response": "",
  "memory_updates": {}
}

FIELD DEFINITIONS

intent:
A short label describing the user's goal.

Examples:
music_control
web_search
open_application
system_control
volume_control
brightness_control
network_control
battery_check
unknown

confidence:
A number between 0 and 1 indicating confidence.

actions:
A list of actions to execute.

response:
A short natural sentence Sparky can speak aloud.

memory_updates:
Information that should be remembered for future requests.

Leave empty when nothing should be remembered.

Example:

{
  "memory_updates": {}
}

or

{
  "memory_updates": {
    "last_app": "spotify"
  }
}

SUPPORTED TOOLS

Application Tools

open_app
Parameters:
app

Website Tools

open_website
Parameters:
website

Search Tools

search_google
Parameters:
query

search_youtube
Parameters:
query

Audio Tools

volume_up
volume_down
mute_volume

Display Tools

brightness_up
brightness_down

Network Tools

wifi_on
wifi_off
wifi_toggle

bluetooth_toggle

System Tools

lock_screen
battery_status

Media Tools

play_pause
next_track
previous_track

Utility Tools

cricket_score

MEMORY RULES

Remember information only when it may be useful later.

Useful examples:

Preferred browser
Preferred music platform
Favorite websites
Frequently used applications
Most recently opened application
Most recently opened website
Most recent search query

Examples:

User:
my preferred browser is firefox

memory_updates:
{
  "preferred_browser": "firefox"
}

User:
open spotify

memory_updates:
{
  "last_app": "spotify"
}

User:
open youtube

memory_updates:
{
  "last_website": "youtube"
}

User:
search youtube for phonk mix

memory_updates:
{
  "last_search": "phonk mix"
}

Do not store temporary conversational details.
Do not store random facts unless they are likely to help future commands.

RULES

1. Return ONLY valid JSON.
2. Use only supported tools.
3. Never invent tools.
4. Extract parameters when required.
5. Multiple actions may be returned.
6. Preserve execution order.
7. Generate a concise spoken response.
8. Update memory when useful.
9. Use conversation history and context when resolving references.
10. If confidence is low, set confidence below 0.5.
11. If no action is possible, return an empty action list.

UNKNOWN REQUEST FORMAT

{
  "intent": "unknown",
  "confidence": 0.2,
  "actions": [],
  "response": "Sorry, I cannot perform that action.",
  "memory_updates": {}
}

EXAMPLES

User:
open spotify

Output:
{
  "intent": "open_application",
  "confidence": 0.99,
  "actions": [
    {
      "tool": "open_app",
      "app": "spotify"
    }
  ],
  "response": "Opening Spotify.",
  "memory_updates": {
    "last_app": "spotify"
  }
}

User:
search google for python decorators

Output:
{
  "intent": "web_search",
  "confidence": 0.99,
  "actions": [
    {
      "tool": "search_google",
      "query": "python decorators"
    }
  ],
  "response": "Searching Google for Python decorators.",
  "memory_updates": {
    "last_search": "python decorators"
  }
}

User:
turn the volume up

Output:
{
  "intent": "volume_control",
  "confidence": 0.98,
  "actions": [
    {
      "tool": "volume_up"
    }
  ],
  "response": "Turning the volume up.",
  "memory_updates": {}
}
"""

# =========================
# LLM CALL
# =========================

def get_actions(user_request: str):

    history = get_memory()

    history_text = ""


    for items in history:
        history_text+= f"""
        User: {items['user']},
        Assistant: {items['assistant']}

        """    

    context = get_context()

    with open("memory/profile.json", "r") as fp:
        profile_data = fp.read()


    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history_text}

context:
{json.dumps(context, indent=2)}

User profile data :
{profile_data}

User Request:
{user_request}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False,
            "temperature": 0,
            "format" : "json"
        }
    )

    raw = response.json()["response"].strip()

    print("\nLLM RAW:")
    print(raw)

    class ModelResponse(BaseModel):
      intent : str
      confidence: float
      actions : list[dict[str, str]]
      response : str
      memory_updates : dict[str,str]

    try:
      data =  json.loads(raw)
      result = ModelResponse(**data)
      data = result.model_dump()

      if(data["confidence"] < 0.80):
        print("Not enough confidence in output")
        data = {
        "actions": [],
        "response": "Sorry, I couldn't understand that."
        }
      print("\nLLM result validated\n")

    except (json.JSONDecodeError, ValidationError):

      print("Invalid JSON returned by model")

      data = {
        "actions": [],
        "response": "Sorry, I couldn't understand that."
      }
    
    print("\nDATA :\n", data)
    return data

# =========================
# EXECUTOR
# =========================

def open_app_tool(action):
    app = action["app"].lower()

    if app in APPS:
        APPS[app]()
    else:
        print(f"Unknown app: {app}")


def open_website_tool(action):
    site = action["website"].lower()

    if site in WEBSITES:
        WEBSITES[site]()
    else:
        print(f"Unknown website: {site}")


TOOLS = {
    "open_app": open_app_tool,
    "open_website": open_website_tool,
    "search_google": lambda a: search_google(a["query"]),
    "search_youtube": lambda a: search_youtube(a["query"]),
    "volume_up": lambda a: volume_up(),
    "volume_down": lambda a: volume_down(),
    "mute_volume": lambda a: mute_volume(),
    "brightness_up": lambda a: brightness_up(),
    "brightness_down": lambda a: brightness_down(),
    "wifi_on": lambda a: wifi_on(),
    "wifi_off": lambda a: wifi_off(),
    "wifi_toggle": lambda a: wifi_toggle(),
    "bluetooth_toggle": lambda a: bluetooth_toggle(),
    "lock_screen": lambda a: lock_screen(),
    "battery_status": lambda a: battery_status(),
    "play_pause": lambda a: play_pause(),
    "next_track": lambda a: next_track(),
    "previous_track": lambda a: previous_track(),
    "cricket_score": lambda a: cricket_score(),
}


def execute_actions(data):
    update_context(data.get("memory_updates", {}))

    for action in data.get("actions", []):
        tool = action.get("tool")

        try:
            if tool in TOOLS:
                TOOLS[tool](action)
            else:
                print(f"Unknown tool: {tool}")

        except Exception as e:
            print(f"Execution error in '{tool}': {e}")

    asyncio.run(speak(data["response"]))
    logger.info(f"LLM OUTPUT : {data['response']}")

# =========================
# MAIN
# =========================
def ask_llm(text):

    data = get_actions(text)

    add_memory(text, data["response"])

    print("\nPARSED:")
    print(json.dumps(data, indent=2))

    execute_actions(data)