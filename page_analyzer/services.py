from validators import url
from urllib.parse import urlparse


def get_site_name(url_string):
    parce_url = urlparse(url_string)

    if parce_url.scheme:
        return f'{parce_url.scheme}://{parce_url.netloc}'
    else:
        return f'https://{parce_url.netloc}'


def validate(url_string):
    norm_url = get_site_name(url_string)
    errors = {}
    if not url(norm_url) or len(norm_url) > 255:
        errors['url'] = 'Некорректный URL'
    return errors
