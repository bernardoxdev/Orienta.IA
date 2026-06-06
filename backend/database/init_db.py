from backend.database.base import Base
from backend.database.connection import engine

import backend.database.models

Base.metadata.create_all(bind=engine)