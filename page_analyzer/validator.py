from validators import url


def validate(url_string):
    errors = {}
    if not url(url_string) or len(url_string) > 255:
        errors['url'] = 'Некорректный URL'
    return errors
