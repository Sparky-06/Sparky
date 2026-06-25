import json

import os
import json

if os.path.exists("history.json"):
    with open("memory/history.json") as fp:
        conversation_history = json.load(fp)
else:
    conversation_history = []



def add_memory(user, assistant):
    conversation_history.append(
        {   "user" : user,
            "assistant" : assistant
        }
    )
        
    if len(conversation_history) > 10:
        conversation_history.pop(0)

    with open("memory/history.json", "w") as fp:
        json.dump(conversation_history, fp)
    

def get_memory():
    return conversation_history