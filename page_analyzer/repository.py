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


class UrlViewRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return connect(self.db_url)

    def get_last_check_data(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    '''
                    SELECT
                        urls.id,
                        urls.url,
                        url_checks.created_at,
                        url_checks.status_code
                    FROM urls
                    LEFT JOIN url_checks
                        ON url_checks.url_id = urls.id
                        AND url_checks.created_at = (
                            SELECT MAX(created_at)
                            FROM url_checks
                            WHERE url_id = urls.id
                        )
                    ORDER BY urls.id DESC;
                    '''
                )
                rows = [dict(row) for row in cur]

        result = []

        for row in rows:
            created_at = row.get('created_at')
            status_code = row.get('status_code')

            if row['created_at']:
                row['created_at'] = created_at.strftime('%Y-%m-%d')
            else:
                row['created_at'] = ''

            if not status_code:
                row['status_code'] = ''

            result.append(row)

        return result
