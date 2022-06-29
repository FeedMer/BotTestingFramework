import os
from sqlalchemy import create_engine

from config.constants import Constants


class DatabaseConfiguration:
    BATCH_SIZE = 1000
    _engine = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                Constants.DB_URL,
                echo=False,
                executemany_mode='values',
                executemany_values_page_size=cls.BATCH_SIZE
            )
        return cls._engine
