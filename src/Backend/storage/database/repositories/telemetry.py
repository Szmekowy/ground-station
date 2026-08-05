from storage.database.models import Telemetry


class TelemetryRepository:

    def __init__(self, session):
        self.session = session


    def save(self, data):

        telemetry = Telemetry(
            timestamp=data["timestamp"],

            x=data["position"]["x"],
            y=data["position"]["y"],
            z=data["position"]["z"],

            battery=data["battery"],
            pressure=data["pressure"],

            raw_data=data
        )

        self.session.add(telemetry)
        self.session.commit()

        return telemetry