import shlex
from app.bot.command_types import Command, HelpCommand
from .add_event import parse_add_event
from .list_events import parse_list_events
from .remove_event import parse_remove_event
from .free_time import parse_free_time
from .update_event import parse_update_event

# remove_all_events is deprecated/merged


def parse_command(text: str) -> Command | None:
    text = text.strip()
    if not text:
        return None

    try:
        parts = shlex.split(text)
    except ValueError:
        return None

    if not parts:
        return None

    cmd_name = parts[0].lower()
    args = parts[1:]

    if cmd_name == "add":
        return parse_add_event(args)
    elif cmd_name == "list":
        return parse_list_events(args)
    elif cmd_name == "remove":
        return parse_remove_event(args)
    elif cmd_name == "free":
        return parse_free_time(args)
    elif cmd_name == "update":
        return parse_update_event(args)
    elif cmd_name == "help":
        return HelpCommand()

    return None
