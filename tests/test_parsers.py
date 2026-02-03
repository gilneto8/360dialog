from datetime import datetime
from app.bot.parsers import parse_command
from app.bot.command_types import (
    AddEventCommand,
    ListEventsCommand,
    RemoveEventCommand,
    RemoveAllEventsCommand,
    FreeTimeCommand,
    HelpCommand,
    UpdateEventCommand,
)


def test_add_valid():
    cmd = parse_command("add --title 'My Meeting' --start 2026-03-02")
    assert isinstance(cmd, AddEventCommand)
    assert cmd.title == "My Meeting"
    assert cmd.start_time.year == 2026
    assert cmd.start_time.month == 3
    assert cmd.start_time.day == 2


def test_add_full():
    cmd = parse_command(
        "add --title 'My Meeting' --start '2026-03-02 10:00' --end '2026-03-02 11:00'"
    )
    assert isinstance(cmd, AddEventCommand)
    assert cmd.start_time == datetime(2026, 3, 2, 10, 0)
    assert cmd.end_time == datetime(2026, 3, 2, 11, 0)


def test_add_weekday():
    cmd = parse_command("add --title 'Meeting' --start Monday")
    assert isinstance(cmd, AddEventCommand)
    assert cmd.start_time.weekday() == 0


def test_add_hour_only():
    cmd = parse_command("add --title 'Meeting' --start 15")
    assert isinstance(cmd, AddEventCommand)
    assert cmd.start_time.hour == 15
    assert cmd.start_time.minute == 0


def test_add_missing_args():
    cmd = parse_command("add --title 'My Meeting'")
    assert cmd is None


def test_list_empty():
    cmd = parse_command("list")
    assert isinstance(cmd, ListEventsCommand)
    assert cmd.start_date is None
    assert cmd.end_date is None


def test_list_dates():
    cmd = parse_command("list --start 2026-03-02 --end 2026-03-05")
    assert isinstance(cmd, ListEventsCommand)
    assert cmd.start_date.date() == datetime(2026, 3, 2).date()
    assert cmd.end_date.date() == datetime(2026, 3, 5).date()


def test_remove_title():
    cmd = parse_command("remove --title 'Bad Event'")
    assert isinstance(cmd, RemoveEventCommand)
    assert cmd.title == "Bad Event"


def test_remove_all():
    cmd = parse_command("remove --all")
    assert isinstance(cmd, RemoveAllEventsCommand)


def test_remove_fail_no_args():
    cmd = parse_command("remove")
    assert cmd is None


def test_free_time():
    cmd = parse_command("free --start 2026-03-02")
    assert isinstance(cmd, FreeTimeCommand)
    assert cmd.start_time.date() == datetime(2026, 3, 2).date()


def test_help():
    cmd = parse_command("help")
    assert isinstance(cmd, HelpCommand)


def test_unknown_command():
    cmd = parse_command("unknown")
    assert cmd is None


def test_update_valid_full():
    cmd = parse_command(
        "update --title 'Old' --new-title 'New' --start '2026-03-02 10:00' --end '2026-03-02 11:00'"
    )
    assert isinstance(cmd, UpdateEventCommand)
    assert cmd.title == "Old"
    assert cmd.new_title == "New"
    assert cmd.start_time == datetime(2026, 3, 2, 10, 0)
    assert cmd.end_time == datetime(2026, 3, 2, 11, 0)


def test_update_partial_title():
    cmd = parse_command("update --title 'Old' --new-title 'New'")
    assert isinstance(cmd, UpdateEventCommand)
    assert cmd.title == "Old"
    assert cmd.new_title == "New"
    assert cmd.start_time is None
    assert cmd.end_time is None


def test_update_partial_time():
    cmd = parse_command("update --title 'Old' --start '2026-03-02 15:00'")
    assert isinstance(cmd, UpdateEventCommand)
    assert cmd.title == "Old"
    assert cmd.new_title is None
    assert cmd.start_time == datetime(2026, 3, 2, 15, 0)


def test_update_missing_title():
    cmd = parse_command("update --new-title 'New'")
    # Title is required
    assert cmd is None
