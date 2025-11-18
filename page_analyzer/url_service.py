from urllib.parse import urlparse

from validators import url


def get_site_name(url_string):
    parce_url = urlparse(url_string)

    if parce_url.scheme:
        return f'{parce_url.scheme}://{parce_url.netloc}'
    else:
        return f'https://{parce_url.path}'


def validate(url_string):
    errors = {}

    if not url(url_string) or len(url_string) > 255:
        errors['url'] = 'Некорректный URL'
    return errors


def datatime_formater(datatime):
    if datatime:
        return datatime.strftime('%Y-%m-%d')
    else:
        return ''
