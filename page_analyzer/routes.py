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
from page_analyzer.repository import UrlRepository


def init_routes(app):
    repo = UrlRepository(app.config['DATABASE_URL'])

    @app.get('/')
    def index():
        return render_template(
            'index.html'
        )

    @app.get('/urls')
    def urls_get():
        urls = repo.get_all()
        return render_template(
            'urls/index.html',
            urls=urls,
        )

    @app.get('/urls/<id>')
    def urls_show(id):
        messages = get_flashed_messages(with_categories=True)
        url_data = repo.find(id)
        return render_template(
            'urls/show.html',
            url=url_data,
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
                messages=messages,
                url=url,
            )

        url = urlparse(url).netloc
        raw_url['url'] = url

        existing_url = repo.find_by_url(url)
        if existing_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', id=existing_url['id']))

        id = repo.save(raw_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_show', id=id))
