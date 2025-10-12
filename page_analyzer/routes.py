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

    @app.route('/urls/<id>')
    def urls_show(id):
        messages = get_flashed_messages(with_categories=True)
        url_data = repo.find(id)
        return render_template(
            'show.html',
            url_data=url_data,
            messages=messages,
        )

    @app.post('/urls')
    def urls_post():
        raw_url = request.form.to_dict()  # {'url': 'https://ya.ru'}
        url = raw_url['url']
        errors = validate(url)
        if errors:
            flash('Некорректный URL', 'fail')
            return (
                redirect(url_for('index'))
            )
        id = repo.save(raw_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_show', id=id))
