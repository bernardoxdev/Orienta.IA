from backend.database.base import Base
from backend.database.connection import engine

Base.metadata.create_all(bind=engine)