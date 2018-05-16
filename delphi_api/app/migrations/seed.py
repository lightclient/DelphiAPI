from app.migrations.models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from datetime import datetime, timedelta

def seed(engine):
    Base.metadata.reflect(bind=engine) # need to figure out what this does
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # new_record = [
    #     User(None, 'john paul', 'onte', 'jnplonte', 'password', 'jnpl.onte@gmail.com', None, func.now()),
    #     User(None, 'first name', 'last name', 'username', 'password', 'email@gmail.com', None, func.now()),
    #     UserActivity('1', '0', '0', '0', func.now()),
    #     UserActivity('2', '0', '0', '0', func.now())
    # ]
    #
    # session.add_all(new_record)

    # Session = sessionmaker(bind=engine)
    # session = Session()

    # s = Stake(
    #     '0x0000000000000000000000000000000000000000',
    #     '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    #     100,
    #     'I love cats',
    #     5,
    #     999999999        #standing in for unix time
    # )
    #
    # w = Whitelistee(
    #     s.address,
    #     '0x0000000000000000000000000000000000000001',
    #     999999999             #standing in for unix time
    # )
    #
    # s.whitelist.append(w)

    # session.add_all([s,w])
    #
    # session.commit()
