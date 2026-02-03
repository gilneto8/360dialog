from sqlalchemy.orm import Session
from app.bot.command_types import AddEventCommand
from app.db.models import Event
from app.bot.handlers.utils import check_overlaps, format_clash_warning


def handle_add_event(command: AddEventCommand, db: Session) -> str:
    clashes = check_overlaps(db, command.start_time, command.end_time)
    warning = format_clash_warning(clashes)

    new_event = Event(
        title=command.title, start_time=command.start_time, end_time=command.end_time
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return f"Event '{new_event.title}' added at {new_event.start_time} {'to ' + str(new_event.end_time) if new_event.end_time else ''}.{warning}"
