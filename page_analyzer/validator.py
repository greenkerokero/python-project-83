from validators import url


def validate(url_string):
    errors = {}
    print(not url(url_string))
    print(len(url_string) > 255)
    if not url(url_string) or len(url_string) > 255:
        errors['url'] = 'Некорректный URL'
    return errors
