from functools import wraps
from datetime import datetime, timedelta
from .cfg import Configuration
from .logger import logger

class Scheduler:
    def __init__(self, db, name):
        self._db = db
        self._name = name
        self._data = dict()

    def schedule(self, slug, *, interval):
        logger.info(f"Scheduler: {self._name} has registered an event: {slug}.")
        self._data[slug] = interval
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                {o(self._name)},
                {o(slug)},
                NULL
            ) ON CONFLICT (slug, name) DO NOTHING
        """)

    def _advance_query(self, o):
        now_dt = datetime.utcnow()
        filters = list()
        cases = list()
        for slug, interval in self._data.items():
            cases.append(f"""
                WHEN name = {o(self._name)} AND slug = {o(slug)}
                THEN {o(now_dt)}
            """)
            filters.append(f"""
                OR name = {o(self._name)} AND slug = {o(slug)} 
                AND (last_run_dt < {o(now_dt - interval)} 
                OR last_run_dt IS NULL)
            """)
        return f"""
            UPDATE {Configuration.table}
            SET last_run_dt = CASE {" ".join(cases)} ELSE last_run_dt END
            WHERE FALSE
            {" ".join(filters)}
            RETURNING *
        """

    def get_pending(self):
        if len(self._data) == 0:
            return
        logger.debug(f"Advancing all registered events.")
        for row in self._db.fetch_all(self._advance_query):
            yield row["slug"]

    @staticmethod
    def setup(db):
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                last_run_dt TIMESTAMP NULL,
                PRIMARY KEY (name, slug)
            )   
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Configuration.table}_name_ix ON
                {Configuration.table}(name);
        """)

    @staticmethod
    def destroy_old_events(db, *, max_age = timedelta(days = 28)):
        cutoff_dt = datetime.utcnow() - max_age
        db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE last_run_dt < {o(cutoff_dt)}
        """)
