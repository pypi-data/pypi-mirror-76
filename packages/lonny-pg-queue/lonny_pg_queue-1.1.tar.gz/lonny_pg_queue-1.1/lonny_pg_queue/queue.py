from .logger import logger
from .cfg import Configuration
from datetime import datetime, timedelta
from contextlib import contextmanager
import json

class Message:
    def __init__(self, db, id, payload):
        self._db = db
        self.id = id
        self.payload = payload

    @contextmanager
    def use(self):
        yield self.payload
        self.consume()

    def consume(self):
        self._db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE id = {o(self.id)}
        """)
        logger.debug(f"Message: {self.id} consumed")

class Queue():
    def __init__(self, db, name):
        self._db = db
        self._name = name

    def put(self, payload, *, attempts = 3):
        logger.info(f"Queue: {self._name} enqueued with message: {json.dumps(payload)}.")
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                DEFAULT,
                {o(self._name)},
                {o(json.dumps(payload))},
                NULL,
                {o(attempts)}
            );
        """)

    def get(self):
        while True:
            now_dt = datetime.utcnow()
            cutoff_dt = now_dt - timedelta(seconds = Configuration.unlock_seconds)
            row = self._db.fetch_one(lambda o: f"""
                UPDATE {Configuration.table} 
                SET lock_dt = {o(now_dt)},
                attempts = attempts - 1
                WHERE id = (
                    SELECT id FROM {Configuration.table}
                    WHERE name = {o(self._name)}
                    AND (lock_dt IS NULL OR lock_dt < {o(cutoff_dt)})
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                ) RETURNING *
            """)
            if row is None:
                return None
            message = Message(self._db, row["id"], row["payload"])
            if row["attempts"] < 0:
                logger.debug(f"Queue: {self._name} has dequeued a message: {message.id} with no more attempts.")
                message.consume()
                continue
            logger.info(f"Queue: {self._name} has dequeued message: {message.id} with payload: {json.dumps(message.payload)}.")
            return message

    @staticmethod
    def setup(db):
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                id SERIAL,
                name TEXT NOT NULL,
                payload JSONB NOT NULL,
                lock_dt TIMESTAMP NULL,
                attempts INTEGER NOT NULL,
                PRIMARY KEY(id)
            );
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Configuration.table}_name_ix
                ON {Configuration.table}(name);
        """)