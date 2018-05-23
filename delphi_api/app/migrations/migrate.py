from app.migrations.models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from datetime import datetime, timedelta

def migrate(engine):
    Base.metadata.reflect(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
