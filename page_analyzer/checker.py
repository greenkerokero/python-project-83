from bs4 import BeautifulSoup
from requests import get as get_request


def check(url):
    url_response = get_request(url)
    response_code = url_response.status_code
    page_content = BeautifulSoup(url_response.text, features="html.parser")

    h1 = page_content.find('h1')
    h1_text = h1.text if h1 else ''

    title = page_content.find('title')
    title_text = title.text if title else ''

    meta_tag = page_content.find('meta', attrs={'name': 'description'})
    description = meta_tag['content'] if meta_tag else ''

    check_result = {
        'status_code': response_code,
        'h1': h1_text,
        'title': title_text,
        'description': description,
    }

    return check_result
