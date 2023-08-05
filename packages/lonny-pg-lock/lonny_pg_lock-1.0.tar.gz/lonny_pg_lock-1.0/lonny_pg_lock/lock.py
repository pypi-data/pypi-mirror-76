from secrets import token_hex
from time import sleep
from contextlib import contextmanager
from datetime import datetime, timedelta
from .cfg import Configuration
from .logger import logger

class Lock:
    def __init__(self, db, name):
        self._db = db
        self._session = token_hex()
        self._name = name

    def acquire(self):
        logger.debug(f"Attempting to acquire lock: {self._name}.")
        now_dt = datetime.utcnow()
        cutoff_dt = now_dt - timedelta(seconds = Configuration.stale_seconds)
        row = self._db.fetch_one(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                {o(self._name)},
                {o(now_dt)},
                {o(self._session)}
            ) ON CONFLICT (name) DO UPDATE
                SET lock_dt = {o(now_dt)}, session = {o(self._session)}
                WHERE {Configuration.table}.lock_dt IS NULL 
                OR {Configuration.table}.lock_dt < {o(cutoff_dt)} 
                OR {Configuration.table}.session = {o(self._session)}
            RETURNING *           
        """)
        is_locked = row is not None
        logger.debug(f"Lock status: {is_locked}.")
        return is_locked

    def release(self):
        logger.debug(f"Releasing lock: {self._name}.")
        self._db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE name = {o(self._name)}
        """  )

    @contextmanager
    def guard(self):
        try:
            yield
        finally:
            self.release()

    @staticmethod
    def setup(db):
        logger.info("Creating lock table.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                name TEXT NOT NULL,
                lock_dt TIMESTAMP NULL,
                session TEXT NULL,
                PRIMARY KEY(name)
            );
        """)

    @staticmethod
    def destroy_old_locks(db, *, max_age = timedelta(days = 90)):
        min_lock_dt = datetime.utcnow() - max_age
        db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE lock_dt < {o(min_lock_dt)}
        """)