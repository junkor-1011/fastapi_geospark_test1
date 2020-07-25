"""database"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# read environment variables (or set default value)
using_db = os.getenv('USING_DB', 'sqlite3')


def create_setting(using_db):
    """
    set the config of sql-alchemy

    set below dynamically:

        - ``SQLALCHEMY_DATABASE_URL`` ,
        - ``engine`` ,
        - ``SessionLocal`` ,
        - ``Base``

    ToDo:

        read from under the ``conf`` .
    """
    if using_db == 'sqlite3' or using_db == 'sqlite':

        SQLALCHEMY_DATABASE_URL = "sqlite:///./data/db/app_sqlite.db"

        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )

    Base = declarative_base()

    return (
        SQLALCHEMY_DATABASE_URL,
        engine,
        SessionLocal,
        Base,
    )


SQLALCHEMY_DATABASE_URL, engine, SessionLocal, Base = create_setting(using_db)
