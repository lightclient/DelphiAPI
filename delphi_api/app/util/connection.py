import logging
import os

from  sqlalchemy import create_engine


def connect():
    if os.environ.get('DB') == "postgres":
        engine = create_engine( "postgresql://%s@%s:%s/%s" %
            (os.environ.get('POSTGRES_USER'),
             os.environ.get('POSTGRES_HOST'),
             os.environ.get('POSTGRES_PORT'),
             os.environ.get('POSTGRES_DB')), echo=False)
    else:
        engine = None

    # logger = logging.getLogger(configs.APP_NAME)
    # logger.info("connected to database")

    return engine
