from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return connect(self.db_url)

    def get_all(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
                return [dict(row) for row in cur]

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                return cur.fetchone()

    def find_by_url(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE url = %s", (url,))
                return cur.fetchone()

    def save(self, url):
        print(url)
        if 'id' in url and url['id']:
            return self._update(url)
        else:
            return self._create(url)

    def _update(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE urls SET url = %s WHERE id = %s',
                    (url['url'], url['id']),
                )
            conn.commit()
            return url['id']

    def _create(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO urls (url) VALUES (%s) RETURNING id',
                    (url['url'],),
                )
                id = cur.fetchone()[0]
                url['id'] = id
            conn.commit()
            return id
