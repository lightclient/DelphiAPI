import logging
import os

from  sqlalchemy import create_engine

def connect():
    if os.environ.get('DATABASE_URL'):
        engine = create_engine( os.environ.get('DATABASE_URL'), echo=False )
    else:
        engine = create_engine( 'postgresql://%s@%s:%s/%s' %
            ('delphi',
             'localhost',
             5432,
             'delphi'), echo=False )

    # logger = logging.getLogger(configs.APP_NAME)
    # logger.info("connected to database")

    return engine
