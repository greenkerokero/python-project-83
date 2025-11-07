from abc import ABC, abstractmethod
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class BaseRepository(ABC):
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return connect(self.db_url)

    @abstractmethod
    def table_name(self):
        pass

    def get_all(self, order_by='created_at DESC'):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    f'SELECT * FROM {self.table_name()} ORDER BY {order_by}'
                )
                return [dict(row) for row in cur]

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    f'SELECT * FROM {self.table_name()} WHERE id = %s',
                    (id,),
                )
                return cur.fetchone()


class UrlRepository(BaseRepository):
    def table_name(self):
        return 'urls'

    def find_by_url(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    f'SELECT * FROM {self.table_name()} WHERE url = %s',
                    (url,),
                )
                return cur.fetchone()

    def save(self, url):
        if 'id' in url and url['id']:
            return self._update(url)
        else:
            return self._create(url)

    def _update(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'UPDATE {self.table_name()} SET url = %s WHERE id = %s',
                    (url['url'], url['id']),
                )
            conn.commit()
            return url['id']

    def _create(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'''
                    INSERT INTO {self.table_name()}
                        (url)
                    VALUES (%s)
                    RETURNING id
                    ''',
                    (url['url'],),
                )
                url_id = cur.fetchone()[0]
                url['id'] = url_id
            conn.commit()
            return url_id


class UrlCheckRepository(BaseRepository):
    def table_name(self):
        return 'url_checks'

    def find_by_url_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    f'SELECT * FROM {self.table_name()} WHERE url_id = %s',
                    (url_id,),
                )
                return [dict(row) for row in cur]

    def get_last_check_time(self, url_id):
        row = self._get_last_check(url_id)
        if row and row['created_at']:
            return row['created_at']
        return None

    def get_last_check_code(self, url_id):
        row = self._get_last_check(url_id)
        if row and row['status_code']:
            return row['status_code']
        return None

    def _get_last_check(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    f'''
                    SELECT *
                    FROM {self.table_name()}
                    WHERE url_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1;
                    ''',
                    (url_id,),
                )
                row = cur.fetchone()
                return row

    def save(self, url_checks):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'''
                    INSERT INTO {self.table_name()}
                        (url_id, status_code, h1, title, description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    ''',
                    (
                        url_checks['url_id'],
                        url_checks.get('status_code'),
                        url_checks.get('h1'),
                        url_checks.get('title'),
                        url_checks.get('description'),
                    ),
                )
                url_id = cur.fetchone()[0]
                url_checks['id'] = url_id
            conn.commit()
            return url_id
