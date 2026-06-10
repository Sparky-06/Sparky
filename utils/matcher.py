from rapidfuzz import process, fuzz
from utils.command_registry import ALL_COMMANDS


def match_command(text):

    commands = list(ALL_COMMANDS.keys())

    match = process.extractOne(
        text,
        commands,
        scorer=fuzz.partial_ratio
    )

    if not match:
        return None

    command, score, _ = match

    print(f"Matched: {command} | Score: {score}")

    if score >= 70:
        return ALL_COMMANDS[command]

    return None