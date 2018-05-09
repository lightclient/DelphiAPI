from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, VARCHAR, DECIMAL, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Stake(Base):
    """ user entity class """
    __tablename__ = 'stake'
    address = Column(VARCHAR(128), primary_key=True)
    staker = Column(VARCHAR(128))
    claimable_stake = Column(DECIMAL(precision=70, scale=30))
    data = Column(VARCHAR(128))
    minimum_fee = Column(DECIMAL(precision=70, scale=30))
    claim_deadline = Column(DECIMAL(precision=70, scale=2))

    # token = Column()
    # arbiter = Column()
    whitelist = relationship('Whitelistee')
    # claims = Column()
    # settlements = Column()

    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address, staker, claimable_stake, data, minimum_fee, claim_deadline):
        self.address = address
        self.staker = staker
        self.claimable_stake = claimable_stake
        self.data = data
        self.minimum_fee = minimum_fee
        self.claim_deadline = claim_deadline

    # def __repr__(self):
    #     return "< stake >"# % (self.image, self.first_name, self.last_name, self.username, self.password, self.email, self.active, self.update_time)

class Whitelistee(Base):
    """ user entity class """
    __tablename__ = 'whitelistee'

    stake = Column(VARCHAR(128), ForeignKey('stake.address'), primary_key=True)
    claimant = Column(VARCHAR(128))
    deadline = Column(DECIMAL(precision=70, scale=2))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, stake, claimant, deadline):
        self.stake = stake
        self.claimant = claimant
        self.deadline = deadline
