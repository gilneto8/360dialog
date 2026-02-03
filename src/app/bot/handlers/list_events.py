from sqlalchemy.orm import Session
from app.bot.command_types import ListEventsCommand
from app.db.models import Event
from app.bot.handlers.utils import check_overlaps


def handle_list_events(command: ListEventsCommand, db: Session) -> str:
    query = db.query(Event)

    if command.start_date:
        query = query.filter(Event.start_time >= command.start_date)
    if command.end_date:
        query = query.filter(Event.start_time <= command.end_date)

    query = query.order_by(Event.start_time)
    events = query.all()
    if not events:
        return "No events found."

    lines = ["*Your Agenda*"]
    current_year = None
    current_month = None

    for event in events:
        clashes = check_overlaps(
            db, event.start_time, event.end_time, exclude_id=event.id
        )

        clash_str = ""
        if clashes:
            clash_titles = [e.title for e in clashes]
            titles_str = ", ".join([f'"{t}"' for t in clash_titles])
            clash_str = f" (Clash with {titles_str})"

        event_year = event.start_time.year
        event_month = event.start_time.strftime("%B")

        if event_year != current_year:
            lines.append(f"\n*{event_year}*")
            current_year = event_year
            current_month = None

        if event_month != current_month:
            lines.append(f"_{event_month}_")
            current_month = event_month

        day = event.start_time.day
        start_str = event.start_time.strftime("%H:%M")
        time_str = start_str
        if event.end_time:
            time_str += f" to {event.end_time.strftime('%H:%M')}"

        lines.append(f"- {day}, {time_str} - {event.title}{clash_str}")

    return "\n".join(lines)
