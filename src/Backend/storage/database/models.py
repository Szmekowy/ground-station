from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Float, JSON


class Base(DeclarativeBase):
    pass



class RawTelemetry(Base):

    __tablename__ = "raw_telemetry"


    id = Column(
        Integer,
        primary_key=True
    )


    timestamp = Column(
        Float,
        nullable=False
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



class ProcessedTelemetry(Base):

    __tablename__ = "processed_telemetry"


    id = Column(
        Integer,
        primary_key=True
    )


    timestamp = Column(
        Float,
        nullable=False
    )


    altitude = Column(
        Float
    )


    battery = Column(
        Float
    )


    pressure = Column(
        Float
    )


    processed_data = Column(
        JSON
    )



# TODO:
# class Alarm(Base):
#     pass


# TODO:
# class Command(Base):
#     pass


# TODO:
# class Log(Base):
#     pass