import app.util.json as json
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, VARCHAR, DECIMAL, BIGINT, BOOLEAN
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

    # many to one relationship to token
    token_id = Column(VARCHAR(128), ForeignKey('token.address'))
    token = relationship('Token', back_populates="stakes")

    # many to one relationship to arbiter
    arbiter_id = Column(VARCHAR(128), ForeignKey('arbiter.address'))
    arbiter = relationship('Arbiter', back_populates="stakes")

    # one to many relationship with whitelistees and claims
    whitelist = relationship('Whitelistee')
    claims = relationship('Claim')
    # settlements = Column()

    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address, staker, token, claimable_stake, data, arbiter, minimum_fee, claim_deadline):
        self.address = address
        self.staker = staker
        self.token = token
        self.claimable_stake = claimable_stake
        self.data = data
        self.arbiter = arbiter
        self.minimum_fee = minimum_fee
        self.claim_deadline = claim_deadline

    def toJSON(self):

        #internal relationships (1 to many)
        whitelist_info = [ el.claimant for el in self.whitelist ]
        claims_info = [
            {'claimant': el.claimant,
             'arbiter' : el.arbiter,
             'surplus_fee': el.surplus_fee,
             'data': el.data,
             'ruling': el.ruling,
             'ruled': el.ruled,
             'settlement_failed': el.settlement_failed
            }
            for el in self.claims ]

        #foreign tables (1 to 1)
        # token_info = session.query(Token).filter_by(address=stake_info.token).first()
        # arbiter_info = session.query(Arbiter).filter_by(address=stake_info.arbiter).first()

        return json.dumps({
            'data': {
                'staker': self.staker,
                'value': self.claimable_stake,
                'token': {
                    'name': self.token.name,
                    'symbol': self.token.symbol,
                    'address': self.token.address
                },
                'minimum_fee': self.minimum_fee,
                'data': self.data,
                'claim_deadline': str( int(Decimal(self.claim_deadline.real)) ),
                'arbiter': {
                    'name': self.arbiter.name,
                    'description': self.arbiter.description,
                    'address': self.arbiter.address
                },
                'whitelisted_claimants': whitelist_info,
                'claims': claims_info,
                'settlements': [
                    {
                      "amount": 10,
                      "staker_agrees": 0,
                      "claimant_agrees": 0
                    }
                ]
            },
            'errors': []
        })
    # def __repr__(self):
    #     return "< stake >"# % (self.image, self.first_name, self.last_name, self.username, self.password, self.email, self.active, self.update_time)

class Whitelistee(Base):
    """ user entity class """
    __tablename__ = 'whitelistee'

    # used for sql alchemy relationships
    _id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)

    stake = Column(VARCHAR(128), ForeignKey('stake.address'))
    claimant = Column(VARCHAR(128))
    deadline = Column(DECIMAL(precision=70, scale=2))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, stake, claimant, deadline):
        self.stake = stake
        self.claimant = claimant
        self.deadline = deadline

class Claim(Base):
    """ user entity class """
    __tablename__ = 'claim'

    # used for sql alchemy relationships
    _id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)

    stake = Column(VARCHAR(128), ForeignKey('stake.address'))
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
    """ user entity class """
    __tablename__ = 'token'

    stakes = relationship("Stake", back_populates="token")

    address = Column(VARCHAR(128), primary_key=True)
    name = Column(VARCHAR(128))
    symbol = Column(VARCHAR(128))
    decimals = Column(DECIMAL(precision=70, scale=30))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address):#, name, symbol, decimals):
        self.address = address
        # self.name = name
        # self.symbol = symbol
        # self.decimals = decimals

class Arbiter(Base):
    """ user entity class """
    __tablename__ = 'arbiter'

    stakes = relationship("Stake", back_populates="arbiter")

    address = Column(VARCHAR(128), primary_key=True)
    name = Column(VARCHAR(128))
    description = Column(VARCHAR(128))
    update_time = Column(TIMESTAMP, server_default=func.now())
    create_time = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, address):#, name, description):
        self.address = address
        # self.name = name
        # self.description = description

