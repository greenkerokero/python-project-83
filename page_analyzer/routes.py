from flask import (
    get_flashed_messages,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from page_analyzer.validator import validate
from page_analyzer.repository import UrlRepository


def init_routes(app):
    repo = UrlRepository(app.config['DATABASE_URL'])

    @app.get('/')
    def index():
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages
        )

    @app.post('/urls')
    def urls_post():
        raw_url = request.form.to_dict()  # {'url': 'https://mail.ru'}
        print(f'raw_url - {raw_url}')
        url = raw_url['url']
        print(f'url - {url}')
        errors = validate(url)
        print(f'errors - {errors}')
        if errors:
            flash('Некорректный URL', 'fail')
            return (
                redirect(url_for('index'))
            )
        repo.save(raw_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('index'))  # изменить на контролер получения старницы с добавленным url
