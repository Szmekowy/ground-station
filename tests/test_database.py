from storage.database.connection import get_session
from storage.database.repositories.telemetry import TelemetryRepository


data = {
    "timestamp": 123456789,

    "position": {
        "x": 10,
        "y": 20,
        "z": 300
    },

    "battery": 90,
    "pressure": 1000
}


session = get_session()

repo = TelemetryRepository(session)

repo.save(data)

session.close()


print("Saved!")