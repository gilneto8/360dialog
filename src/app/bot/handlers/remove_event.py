from sqlalchemy.orm import Session
from app.bot.command_types import RemoveEventCommand
from app.db.models import Event


def handle_remove_event(command: RemoveEventCommand, db: Session) -> str:
    event = db.query(Event).filter(Event.title == command.title).first()
    if not event:
        return f"Event '{command.title}' not found."
    db.delete(event)
    db.commit()
    return f"Event '{command.title}' removed."
