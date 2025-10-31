from bs4 import BeautifulSoup
from requests import (
    get as get_request,
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout,
)


def check(url):
    try:
        url_response = get_request(url, timeout=5)
    except ConnectionError:
        return {'error': 'Ошибка подключения'}
    except HTTPError as e:
        return {'error': f'HTTP ошибка: {e.response.status_code}'}
    except TooManyRedirects:
        return {'error': 'Слишком много перенаправлений'}
    except Timeout:
        return {'error': 'Время ожидания запроса истекло'}
    except Exception as e:
        return {'error': f'Непредвиденная ошибка: {e}'}
    else:
        response_code = url_response.status_code
        page_content = BeautifulSoup(url_response.text, features="html.parser")

        h1 = page_content.find('h1')
        h1_text = h1.text if h1 else ''

        title = page_content.find('title')
        title_text = title.text if title else ''

        meta_tag = page_content.find('meta', attrs={'name': 'description'})
        description = meta_tag['content'] if meta_tag else ''

        return {
                'status_code': response_code,
                'h1': h1_text,
                'title': title_text,
                'description': description,
            }
