import app.util.json as json
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

    tok = Token(
        '0x0000000000000000000000000000000000000333',
        'test-token',
        'test-symbol',
        2.0
    )

    arb = Arbiter(
        '0x0000000000000000000000000000000000000334'#,
        #'AVGTBAS Arbitration',
        #'A very good TCR-based arbiter set'
    )


    sta = Stake(
        address='0x0000000000000000000000000000000000000000',
        staker='0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
        token=tok,
        claimable_stake=100,
        data='I love cats',
        minimum_fee=.5,
        arbiter=arb,
        claim_deadline=999999999        #standing in for unix time
    )

    whi = Whitelistee(
         sta.address,
         '0x0000000000000000000000000000000000000001',
         999999999             #standing in for unix time
    )

    cla = Claim(
        sta.address,
        0,
        'Angry guy',
        23.5,
        arb.address,
        .65,
        .05,
        'You owe me money?',
        0,
        False,
        True
    )

    sta.whitelist.append(whi)
    sta.claims.append(cla)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([tok, arb])

    session.commit()

    session.add_all([sta,whi, cla])

    session.commit()

    #print(json.objToJSON(sta, 'stakes'))
