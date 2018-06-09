import app.util.json as json
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, VARCHAR, DECIMAL, BIGINT, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from eth_utils import to_checksum_address

Base = declarative_base()

class Stake(Base):
    """
    ORM class defining the Stake relation in the database
    """

    __tablename__ = 'stake'

    address = Column(VARCHAR(128), primary_key=True)
    staker = Column(VARCHAR(128))
    claimable_stake = Column(DECIMAL(precision=70, scale=30))
    data = Column(VARCHAR(128))
    minimum_fee = Column(DECIMAL(precision=70, scale=30))
    claim_deadline = Column(DECIMAL(precision=70, scale=2))

    # many to one relationship to token
    token_id = Column(VARCHAR(128), ForeignKey('token.address'))
    token = relationship('Token', back_populates="stakes")

    # many to one relationship to arbiter
    arbiter_id = Column(VARCHAR(128), ForeignKey('arbiter.address'))
    arbiter = relationship('Arbiter', back_populates="stakes")

    # one to many relationship with whitelistees and claims
    whitelist = relationship('Whitelistee')
    claims = relationship('Claim')

    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address, staker, token, claimable_stake, data, arbiter, minimum_fee, claim_deadline):
        self.address = to_checksum_address(address)
        self.staker = to_checksum_address(staker)
        self.token = token
        self.claimable_stake = claimable_stake
        self.data = data
        self.arbiter = arbiter
        self.minimum_fee = minimum_fee
        self.claim_deadline = claim_deadline

    def toJSON(self):
        obj = {
            'data': {
                'staker': self.staker,
                'claimable_stake': self.claimable_stake,
                'token': {
                    'name': self.token.name,
                    'symbol': self.token.symbol,
                    'address': self.token.address
                },
                'minimum_fee': self.minimum_fee,
                'data': self.data,
                'claim_deadline': str( int(Decimal(self.claim_deadline.real)) ),
                'arbiter': {
                    'name': '',
                    'description': '',
                    'address': self.arbiter.address
                },
                'whitelist': [w.claimant for w in self.whitelist],
                'claims': [json.loads(c.toJSON()) for c in self.claims],
                'settlements': [] # TODO
            },
            'errors': []
        }

        return json.dumps(obj)


class Whitelistee(Base):
    """
    ORM class defining the Whitelistee relation in the database
    """

    __tablename__ = 'whitelistee'

    # used for sql alchemy relationships
    _id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)

    stake = Column(VARCHAR(128), ForeignKey('stake.address'))
    claimant = Column(VARCHAR(128))
    deadline = Column(DECIMAL(precision=70, scale=2))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, stake, claimant, deadline):
        self.stake = to_checksum_address(stake)
        self.claimant = to_checksum_address(claimant)
        self.deadline = deadline


class Claim(Base):
    """
    ORM class defining the Claim relation in the database
    """

    __tablename__ = 'claim'

    # used for sql alchemy relationships
    _id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)

    stake = Column(VARCHAR(128), ForeignKey('stake.address'))
    settlements = relationship('Settlement')

    id = Column(INTEGER)
    claimant = Column(VARCHAR(128))
    amount = Column(DECIMAL(precision=70, scale=30))
    arbiter = Column(VARCHAR(128), ForeignKey('arbiter.address'))
    fee = Column(DECIMAL(precision=70, scale=30))
    surplus_fee = Column(DECIMAL(precision=70, scale=30))
    data = Column(VARCHAR(128))
    ruling = Column(DECIMAL(precision=70, scale=30)) # TODO make small int
    ruled = Column(BOOLEAN)
    settlement_failed = Column(BOOLEAN)
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, stake, id, claimant, amount, arbiter, fee, surplus_fee, data, ruling, ruled, settlement_failed):
        self.stake = to_checksum_address(stake)
        self.id = id
        self.claimant = to_checksum_address(claimant)
        self.amount = amount
        self.arbiter = to_checksum_address(arbiter)
        self.fee = fee
        self.surplus_fee = surplus_fee
        self.data = data
        self.ruling = ruling
        self.ruled = ruled
        self.settlement_failed = settlement_failed


class Settlement(Base):
    """
    ORM class defining the Settlement relation in the database
    """

    __tablename__ = 'settlement'

    # used for sql alchemy relationships
    _id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)

    stake = Column(VARCHAR(128), ForeignKey('stake.address'))
    claim = Column(INTEGER, ForeignKey('claim._id'))

    id = Column(INTEGER)
    amount = Column(DECIMAL(precision=70, scale=30))
    stakerAgrees = Column(BOOLEAN)
    claimantAgrees = Column(BOOLEAN)

    def __init__(self, stake, id, claimant, amount, arbiter, fee, surplus_fee, data, ruling, ruled, settlement_failed):
        self.stake = stake
        self.id = id
        self.claimant = claimant
        self.amount = amount
        self.arbiter = arbiter
        self.fee = fee
        self.surplus_fee = surplus_fee
        self.data = data
        self.ruling = ruling
        self.ruled = ruled
        self.settlement_failed = settlement_failed


class Token(Base):
    """
    ORM class defining the Token relation in the database
    """

    __tablename__ = 'token'

    stakes = relationship("Stake", back_populates="token")

    address = Column(VARCHAR(128), primary_key=True)
    name = Column(VARCHAR(128))
    symbol = Column(VARCHAR(128))
    decimals = Column(DECIMAL(precision=70, scale=30))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address, name, symbol, decimals):
        self.address = to_checksum_address(address)
        self.name = name
        self.symbol = symbol
        self.decimals = decimals


class Arbiter(Base):
    """
    ORM class defining the Arbiter relation in the database
    """

    __tablename__ = 'arbiter'

    stakes = relationship("Stake", back_populates="arbiter")

    address = Column(VARCHAR(128), primary_key=True)
    name = Column(VARCHAR(128))
    description = Column(VARCHAR(128))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address):#, name, description):
        self.address = to_checksum_address(address)
        # self.name = name
        # self.description = description
