import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Event
from app.bot.command_types import AddEventCommand, ListEventsCommand, UpdateEventCommand
from app.bot.handlers import execute_command


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


def test_add_event_clash(db_session):
    cmd_a = AddEventCommand(
        title="Event A",
        start_time=datetime(2025, 1, 1, 10, 0),
        end_time=datetime(2025, 1, 1, 11, 0),
    )
    execute_command(cmd_a, db_session)

    cmd_b = AddEventCommand(
        title="Event B",
        start_time=datetime(2025, 1, 1, 11, 0),
        end_time=datetime(2025, 1, 1, 12, 0),
    )
    res_b = execute_command(cmd_b, db_session)
    assert "Clash" not in res_b

    cmd_c = AddEventCommand(
        title="Event C",
        start_time=datetime(2025, 1, 1, 10, 30),
        end_time=datetime(2025, 1, 1, 11, 30),
    )
    res_c = execute_command(cmd_c, db_session)
    assert "Clashes with 'Event A'" in res_c


def test_list_events_clash(db_session):
    cmd_a = AddEventCommand(
        title="Event A",
        start_time=datetime(2025, 1, 1, 10, 0),
        end_time=datetime(2025, 1, 1, 11, 0),
    )
    execute_command(cmd_a, db_session)

    cmd_c = AddEventCommand(
        title="Event C",
        start_time=datetime(2025, 1, 1, 10, 30),
        end_time=datetime(2025, 1, 1, 11, 30),
    )
    execute_command(cmd_c, db_session)

    cmd_list = ListEventsCommand()
    res = execute_command(cmd_list, db_session)

    assert "Event A" in res
    assert "Event C" in res
    assert '(Clash with "Event C")' in res
    assert '(Clash with "Event A")' in res


def test_update_event(db_session):
    cmd_x = AddEventCommand(
        title="Event X",
        start_time=datetime(2025, 1, 1, 10, 0),
        end_time=datetime(2025, 1, 1, 11, 0),
    )
    execute_command(cmd_x, db_session)

    cmd_update = UpdateEventCommand(
        title="Event X",
        new_title="Event Y",
        start_time=datetime(2025, 1, 1, 12, 0),
        end_time=datetime(2025, 1, 1, 13, 0),
    )
    res = execute_command(cmd_update, db_session)

    assert "Event updated" in res
    assert "Event Y" in res

    events = db_session.query(Event).all()
    assert len(events) == 1
    assert events[0].title == "Event Y"
    assert events[0].start_time == datetime(2025, 1, 1, 12, 0)


def test_update_event_clash(db_session):
    execute_command(
        AddEventCommand(
            title="Event A",
            start_time=datetime(2025, 1, 1, 10, 0),
            end_time=datetime(2025, 1, 1, 11, 0),
        ),
        db_session,
    )
    execute_command(
        AddEventCommand(
            title="Event B",
            start_time=datetime(2025, 1, 1, 12, 0),
            end_time=datetime(2025, 1, 1, 13, 0),
        ),
        db_session,
    )

    cmd_update = UpdateEventCommand(
        title="Event B", start_time=datetime(2025, 1, 1, 10, 30)
    )
    res = execute_command(cmd_update, db_session)

    assert "Clashes with 'Event A'" in res

    b = db_session.query(Event).filter(Event.title == "Event B").first()
    assert b.start_time == datetime(2025, 1, 1, 10, 30)


def test_update_not_found(db_session):
    cmd = UpdateEventCommand(title="NonExistent", new_title="Exists")
    res = execute_command(cmd, db_session)
    assert "not found" in res


def test_update_partial_persistence(db_session):
    execute_command(
        AddEventCommand(
            title="Original",
            start_time=datetime(2025, 1, 1, 10, 0),
            end_time=datetime(2025, 1, 1, 11, 0),
        ),
        db_session,
    )

    cmd = UpdateEventCommand(title="Original", start_time=datetime(2025, 1, 1, 10, 30))
    execute_command(cmd, db_session)

    event = db_session.query(Event).filter(Event.title == "Original").first()
    assert event.start_time == datetime(2025, 1, 1, 10, 30)
    assert event.end_time == datetime(2025, 1, 1, 11, 0)


def test_update_inverted_timestamps(db_session):
    execute_command(
        AddEventCommand(
            title="Inverted",
            start_time=datetime(2025, 1, 1, 10, 0),
            end_time=datetime(2025, 1, 1, 11, 0),
        ),
        db_session,
    )

    cmd = UpdateEventCommand(title="Inverted", start_time=datetime(2025, 1, 1, 12, 0))
    res = execute_command(cmd, db_session)

    assert "Event updated" in res

    event = db_session.query(Event).filter(Event.title == "Inverted").first()
    assert event.start_time > event.end_time
