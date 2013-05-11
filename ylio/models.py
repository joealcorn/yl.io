from string import ascii_letters, digits

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

    alphabet = digits + ascii_letters

    @classmethod
    def connect(self):
        self.conn = psycopg2.connect(
            database=DB_NAME,
            user=PG_USER,
            password=PG_PASS,
            host=PG_HOST,
            port=PG_PORT
        )
        return self.conn

    @classmethod
    def cursor(self):
        """
        Returns a psycopg2 DictCursor
        """
        return self.connect().cursor(cursor_factory=DictCursor)

    @classmethod
    def new(self, link, ip_address):
        """
        Creates a new shortened URL, returns base36 ID upon success
        """
        cur = self.cursor()
        try:
            cur.execute(
                """
                INSERT INTO links
                (target, created_by) VALUES
                (%s, %s)
                RETURNING id
                """, (link, ip_address)
            )
            int_id = cur.fetchone()[0]
            id36 = self.to_base36(int_id)

            cur.execute(
                """
                UPDATE links SET id36 = %s
                WHERE id = %s
                """, (id36, int_id)
            )
            self.conn.commit()
            cur.close()
            return id36
        except Exception as e:
            print e
            self.conn.rollback()
            cur.close()
            return

    @classmethod
    def get(self, id36):
        """
        Grabs a link from the db by id36
        """
        cur = self.cursor()
        cur.execute(
            """
            SELECT * FROM links
            WHERE id36 = %s
            """, (id36,)
        )
        result = cur.fetchone()
        cur.close()
        return result

    @classmethod
    def disable(self, id36):
        """
        Disables the link with matching id36
        """
        cur = self.cursor()
        cur.execute(
            """
            UPDATE links
            SET active = FALSE
            WHERE id36 = %s
            """, (id36,)
        )
        self.conn.commit()
        cur.close()

    @classmethod
    def to_base36(self, number):
        """
        Converts an integer to a base36 string
        """
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')

        base36 = ''

        if 0 <= number < len(self.alphabet):
            return self.alphabet[number]

        while number != 0:
            number, i = divmod(number, len(self.alphabet))
            base36 = self.alphabet[i] + base36

        return base36
