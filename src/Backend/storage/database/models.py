from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Float, DateTime, JSON


class Base(DeclarativeBase):
    pass



class Telemetry(Base):

    __tablename__ = "telemetry"


    id = Column(
        Integer,
        primary_key=True
    )


    timestamp = Column(
        Float
    )


    x = Column(
        Float
    )


    y = Column(
        Float
    )


    z = Column(
        Float
    )


    battery = Column(
        Float
    )


    pressure = Column(
        Float
    )


    raw_data = Column(
        JSON
    )