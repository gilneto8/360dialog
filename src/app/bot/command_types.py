from abc import ABC
from datetime import datetime
from pydantic import BaseModel


class Command(BaseModel, ABC):
    pass


class AddEventCommand(Command):
    title: str
    start_time: datetime
    end_time: datetime | None = None


class RemoveEventCommand(Command):
    title: str


class RemoveAllEventsCommand(Command):
    pass


class FreeTimeCommand(Command):
    start_time: datetime
    end_time: datetime | None = None


class ListEventsCommand(Command):
    start_date: datetime | None = None
    end_date: datetime | None = None


class HelpCommand(Command):
    pass


class UpdateEventCommand(Command):
    title: str
    new_title: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
