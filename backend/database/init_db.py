from backend.database.base import Base
from backend.database.connection import engine

from backend.database.models.user import User

Base.metadata.create_all(bind=engine)