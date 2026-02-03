from sqlalchemy.orm import Session
from app.bot.command_types import UpdateEventCommand
from app.db.models import Event
from app.bot.handlers.utils import check_overlaps, format_clash_warning


def handle_update_event(command: UpdateEventCommand, db: Session) -> str:
    event = db.query(Event).filter(Event.title == command.title).first()
    if not event:
        return f"Event '{command.title}' not found."

    new_title = command.new_title if command.new_title else event.title
    start_time = command.start_time if command.start_time else event.start_time
    end_time = command.end_time if command.end_time else event.end_time

    clashes = check_overlaps(db, start_time, end_time, exclude_id=event.id)
    warning = format_clash_warning(clashes)

    event.title = new_title
    event.start_time = start_time
    event.end_time = end_time

    db.commit()
    db.refresh(event)

    return f"Event updated. '{event.title}' is now at {event.start_time} {'to ' + str(event.end_time) if event.end_time else ''}.{warning}"
