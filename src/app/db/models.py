from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from app.db.session import engine

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    start_time: datetime = Column(DateTime)
    end_time: datetime = Column(DateTime, nullable=True)
    description: str | None = Column(String, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)
