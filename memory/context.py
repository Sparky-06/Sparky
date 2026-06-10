import json



import os
import json

DEFAULT_CONTEXT = {
    "last_app": None,
    "last_website": None,
    "last_search": None
}

if os.path.exists("context.json"):
    with open("context.json") as fp:
        context = json.load(fp)
else:
    context = DEFAULT_CONTEXT.copy()



# def add_context(action, name):
#     if action == "app":
#         context["last_app"] = name
    
#     if action == "website":
#         context["last_website"] = name
    
#     if action == "search":
#         context["last_search"] = name


def get_context():
    return context


def update_context(data):
    for key, value in data.items():
        if key in context:
            context[key] = value
    
    with open("context.json", "w") as fp:
        json.dump(context, fp)