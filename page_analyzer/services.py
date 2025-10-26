from validators import url
from urllib.parse import urlparse


def normalize(url_string):
    parce_url = urlparse(url_string)

    if parce_url.scheme:
        return url_string
    else:
        return f'https://{url_string}'


def validate(url_string):
    norm_url = normalize(url_string)
    errors = {}
    if not url(norm_url) or len(norm_url) > 255:
        errors['url'] = 'Некорректный URL'
    return errors
