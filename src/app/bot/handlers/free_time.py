from datetime import datetime
from sqlalchemy.orm import Session
from app.bot.command_types import FreeTimeCommand
from app.db.models import Event


def handle_free_time(command: FreeTimeCommand, db: Session) -> str:
    """Find and display free timespans within the given date range."""
    # Query events that overlap with the requested range
    events = (
        db.query(Event)
        .filter(
            Event.start_time < command.end_time,
            (Event.end_time.is_(None)) | (Event.end_time > command.start_time),
        )
        .order_by(Event.start_time)
        .all()
    )

    if not events:
        return f"You are completely free from {_format_dt(command.start_time)} to {_format_dt(command.end_time)}."

    # Calculate free slots
    free_slots: list[tuple[datetime, datetime]] = []
    current_time = command.start_time

    for event in events:
        # Determine the effective start/end of this event within our range
        event_start = max(event.start_time, command.start_time)
        event_end = event.end_time if event.end_time else event.start_time

        # If there's a gap before this event, it's free time
        if event_start > current_time:
            free_slots.append((current_time, event_start))

        # Move current_time forward past this event
        if event_end > current_time:
            current_time = event_end

    # Check for free time after the last event
    if current_time < command.end_time:
        free_slots.append((current_time, command.end_time))

    if not free_slots:
        return f"No free time between {_format_dt(command.start_time)} and {_format_dt(command.end_time)}."

    # Format output
    lines = [
        f"*Free timespans from {_format_dt(command.start_time)} to {_format_dt(command.end_time)}:*"
    ]
    for start, end in free_slots:
        lines.append(f"- {_format_dt(start)} to {_format_dt(end)}")

    return "\n".join(lines)


def _format_dt(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%b %d, %H:%M")
