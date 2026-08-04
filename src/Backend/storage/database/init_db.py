from models import Base
from connection import engine


Base.metadata.create_all(
    engine
)


print("Tables created")