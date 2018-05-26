import logging
import os

from  sqlalchemy import create_engine


def connect():
    if os.environ.get('ENV') == 'DEV':
        engine = create_engine( 'postgresql://%s@%s:%s/%s' %
            (os.environ.get('POSTGRES_USER'),
             os.environ.get('POSTGRES_HOST'),
             os.environ.get('POSTGRES_PORT'),
             os.environ.get('POSTGRES_DB')), echo=False )
    else:
        engine = create_engine( os.environ.get('DATABASE_URL'), echo=False )

    # logger = logging.getLogger(configs.APP_NAME)
    # logger.info("connected to database")

    return engine
