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
from page_analyzer.checker import check
from page_analyzer.repository import UrlRepository, UrlCheckRepository


def init_routes(app):
    url_repo = UrlRepository(app.config['DATABASE_URL'])
    url_check_repo = UrlCheckRepository(app.config['DATABASE_URL'])

    alert_classes = {
        'success': 'success',
        'info': 'info',
        'danger': 'danger'
    }

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
            last_check_time = url_check_repo.get_last_check_time(url.get('id'))
            if last_check_time:
                last_check_time = last_check_time.strftime('%Y-%m-%d')
            else:
                last_check_time = ''

            last_check_code = url_check_repo.get_last_check_code(url.get('id'))
            if not last_check_code:
                last_check_code = ''

            site = {
                'id': url['id'],
                'site': url['url'],
                'last_check': last_check_time,
                'code': last_check_code,
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
            alert_classes=alert_classes,
        )

    @app.post('/urls')
    def urls_post():
        form_data = request.form.to_dict()
        url = form_data['url']
        errors = validate(url)
        if errors:
            flash('Некорректный URL', 'danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template(
                'index.html',
                url=url,
                messages=messages,
                alert_classes=alert_classes,
            )

        scheme = urlparse(url).scheme
        netloc = urlparse(url).netloc
        form_data['url'] = f'{scheme}://{netloc}'

        existing_url = url_repo.find_by_url(url)
        if existing_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', id=existing_url['id']))

        id = url_repo.save(form_data)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_show', id=id))

    @app.post('/urls/<id>/checks')
    def urls_check(id):
        saved_url = url_repo.find(id).get('url')

        check_result = check(saved_url)
        if 'error' in check_result:
            flash(
                f'Не удалось проверить старницу: "{check_result['error']}"',
                'danger'
            )
        else:
            check_data = {
                'url_id': id,
            }
            check_data.update(check_result)
            url_check_repo.save(check_data)
            flash('Страница успешно проверена', 'success')

        return redirect(url_for('urls_show', id=id))
