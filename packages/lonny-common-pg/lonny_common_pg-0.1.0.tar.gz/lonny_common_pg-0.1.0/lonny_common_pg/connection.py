from contextlib import contextmanager
from lonny_common_sql import build
from psycopg2 import connect
from psycopg2.extras import DictCursor
from re import sub
from .logger import logger

class Connection():
    def __init__(self, *, dbname, host, user = "postgres", port = 5432, password = None):
        self._dbname = dbname
        self._host = host
        self._user = user
        self._port = port
        self._password = password
        self._connection = None

    def init(self):
        if self._connection is not None:
            return
        self._connection = connect(
            dbname = self._dbname,
            host = self._host,
            user = self._user,
            port = self._port,
            password = self._password,
            cursor_factory = DictCursor
        )
        self._tx_depth = 0
        self._connection.autocommit = True
        logger.info(f"Connected to database: {self._dbname}.")

    def close(self):
        if self._connection is None:
            return
        self._connection.close()
        self._connection = None
        logger.info(f"Disconnected from database: {self._dbname}.")

    def _get_savepoint(self):
        return f"savepoint_{self._tx_depth}"

    def _build(self, query):
        if callable(query):
            return build(query)
        return query, dict()

    def _trim_sql(self, sql):
        return sub("\s\s+", " ", sql.decode("utf-8")).strip()

    @property
    def open(self):
        return self._connection is not None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    @contextmanager
    def transaction(self):
        self._tx_depth += 1
        savepoint = self._get_savepoint()
        sql = f"SAVEPOINT {savepoint}" if self._tx_depth > 1 else "BEGIN TRANSACTION"
        self.execute(sql)
        try:
            yield
            sql = f"RELEASE SAVEPOINT {savepoint}" if self._tx_depth > 1 else "COMMIT TRANSACTION"
            self.execute(sql)
        except Exception:
            sql = f"ROLLBACK TO SAVEPOINT {savepoint}" if self._tx_depth > 1 else "ROLLBACK TRANSACTION"
            self.execute(sql)
            raise
        finally:
            self._tx_depth -= 1

    def execute(self, query):
        self.init()
        sql, params = self._build(query)
        with self._connection.cursor() as cur:
            sql = self._trim_sql(cur.mogrify(sql, params))
            logger.debug(f"Executing: {sql}")
            cur.execute(sql)

    def fetch_one(self, query):
        self.init()
        sql, params = self._build(query)
        with self._connection.cursor() as cur:
            sql = self._trim_sql(cur.mogrify(sql, params))
            logger.debug(f"Fetching single row: {sql}.")
            cur.execute(sql)
            return cur.fetchone()

    def fetch_all(self, query):
        self.init()
        sql, params = self._build(query)
        with self._connection.cursor() as cur:
            sql = self._trim_sql(cur.mogrify(sql, params))
            logger.debug(f"Fetching multiple rows: {sql}.")
            cur.execute(sql)
            return cur.fetchall()