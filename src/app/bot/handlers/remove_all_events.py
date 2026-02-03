from sqlalchemy.orm import Session
from app.db.models import Event


def handle_remove_all_events(db: Session) -> str:
    db.query(Event).delete()
    db.commit()
    return "All events removed."
