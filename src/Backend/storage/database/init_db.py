from models import Base, RawTelemetry, ProcessedTelemetry
from connection import engine


Base.metadata.create_all(
    engine
)


print("Tables created")