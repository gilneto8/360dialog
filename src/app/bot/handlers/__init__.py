from sqlalchemy.orm import Session
from app.bot.command_types import (
    Command,
    AddEventCommand,
    ListEventsCommand,
    RemoveEventCommand,
    RemoveAllEventsCommand,
    FreeTimeCommand,
    HelpCommand,
    UpdateEventCommand,
)
from .add_event import handle_add_event
from .list_events import handle_list_events
from .remove_event import handle_remove_event
from .remove_all_events import handle_remove_all_events
from .free_time import handle_free_time
from .help import handle_help
from .update_event import handle_update_event


def execute_command(command: Command, db: Session) -> str:
    if isinstance(command, AddEventCommand):
        return handle_add_event(command, db)
    elif isinstance(command, ListEventsCommand):
        return handle_list_events(command, db)
    elif isinstance(command, RemoveEventCommand):
        return handle_remove_event(command, db)
    elif isinstance(command, RemoveAllEventsCommand):
        return handle_remove_all_events(db)
    elif isinstance(command, FreeTimeCommand):
        return handle_free_time(command, db)
    elif isinstance(command, HelpCommand):
        return handle_help()
    elif isinstance(command, UpdateEventCommand):
        return handle_update_event(command, db)
    else:
        return "Unknown command."
