from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return connect(self.db_url)

    def get_connect(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT * FROM urls')
                return [dict(row) for row in cur]

    def save(self, url):
        if 'id' in url and url['id']:
            self._update(url)
        else:
            self._create(url)

    def _update(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE urls SET name = %s WHERE id = %s',
                    (url['name'], url['id']),
                )

    def _create(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                    (url['name']),
                )
                id = cur.fetchone()[0]
                url['id'] = id
            conn.commit()
