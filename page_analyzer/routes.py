from flask import (
    get_flashed_messages,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from urllib.parse import urlparse
from page_analyzer.validator import validate
from page_analyzer.repository import UrlRepository, UrlCheckRepository


def init_routes(app):
    url_repo = UrlRepository(app.config['DATABASE_URL'])
    url_check_repo = UrlCheckRepository(app.config['DATABASE_URL'])

    @app.get('/')
    def index():
        return render_template(
            'index.html'
        )

    @app.get('/urls')
    def urls_get():
        urls = url_repo.get_all()
        sites = []
        for url in urls:
            last_check = url_check_repo.get_last_check(url.get('id'))
            if last_check:
                last_check = last_check.strftime('%Y-%m-%d')
            else:
                last_check = ''

            site = {
                'id': url['id'],
                'site': url['url'],
                'last_check': last_check,
                'code': '',
            }
            sites.append(site)
        return render_template(
            'urls/index.html',
            urls=sites,
        )

    @app.get('/urls/<id>')
    def urls_show(id):
        messages = get_flashed_messages(with_categories=True)
        url = url_repo.find(id)
        checks = url_check_repo.find_by_url_id(id)
        return render_template(
            'urls/show.html',
            url=url,
            checks=checks,
            messages=messages,
        )

    @app.post('/urls')
    def urls_post():
        raw_url = request.form.to_dict()  # {'url': 'https://ya.ru'}
        url = raw_url['url']

        errors = validate(url)
        if errors:
            flash('Некорректный URL', 'fail')
            messages = get_flashed_messages(with_categories=True)
            return render_template(
                'index.html',
                url=url,
                messages=messages,
            )

        url = urlparse(url).netloc
        raw_url['url'] = url

        existing_url = url_repo.find_by_url(url)
        if existing_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', id=existing_url['id']))

        id = url_repo.save(raw_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_show', id=id))

    @app.post('/urls/<id>/checks')
    def urls_check(id):
        check = {
            'url_id': id,
        }
        url_check_repo.save(check)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('urls_show', id=id))
