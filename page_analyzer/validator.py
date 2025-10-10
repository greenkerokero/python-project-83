from validators import url


def validate(url_string):
    errors = {}
    if not url(url_string):
        errors['url'] = 'Некорректный URL'
    return errors
