import psycopg2
from psycopg2.extras import DictCursor

from ylio.config import (
    PG_HOST,
    PG_PORT,
    DB_NAME,
    PG_USER,
    PG_PASS
)


class Links(object):

    conn = psycopg2.connect(
        database=DB_NAME,
        user=PG_USER,
        password=PG_PASS,
        host=PG_HOST,
        port=PG_PORT
    )

    @classmethod
    def cursor(self):
        return self.conn.cursor(cursor_factory=DictCursor)
