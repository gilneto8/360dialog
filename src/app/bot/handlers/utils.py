from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Event


def check_overlaps(
    db: Session, start: datetime, end: datetime | None, exclude_id: int | None = None
) -> list[Event]:
    query = db.query(Event)

    filters = []

    if end is not None:
        filters.append(Event.start_time < end)

    filters.append((Event.end_time.is_(None)) | (Event.end_time > start))

    if exclude_id is not None:
        filters.append(Event.id != exclude_id)

    return query.filter(*filters).all()


def format_clash_warning(clashes: list[Event]) -> str:
    if not clashes:
        return ""
    titles = [f"'{e.title}'" for e in clashes]
    return f" Warning: Clashes with {', '.join(titles)}."
