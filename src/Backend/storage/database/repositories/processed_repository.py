from storage.database.models import ProcessedTelemetry


class ProcessedRepository:

    def __init__(self, session):
        self.session = session


    def save(self, data):

        processed = ProcessedTelemetry(

            timestamp=data["timestamp"],

            altitude=data["altitude"],

            battery=data["battery"],

            pressure=data["pressure"],

            processed_data=data
        )


        self.session.add(processed)

        self.session.commit()


        return processed