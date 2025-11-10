from flask import (
    get_flashed_messages,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
    current_app
)
from page_analyzer.services import validate, get_site_name
from page_analyzer.parser import parse


bp = Blueprint('urls', __name__)

ALERT_CLASSES = {
    'success': 'success',
    'info': 'info',
    'danger': 'danger'
}


@bp.get('/urls')
def urls_get():
    url_repo = current_app.url_repo
    url_check_repo = current_app.url_check_repo

    urls = url_repo.get_all()
    sites = []
    for url in urls:
        last_check_data = url_check_repo.get_last_check_data(url.get('id'))
        site = {
            'id': url['id'],
            'site': url['url'],
        }
        site.update(last_check_data)
        sites.append(site)

    return render_template(
        'urls/index.html',
        urls=sites,
    )


@bp.get('/urls/<id>')
def urls_show(id):
    url_repo = current_app.url_repo
    url_check_repo = current_app.url_check_repo

    messages = get_flashed_messages(with_categories=True)
    url = url_repo.find(id)
    checks = url_check_repo.find_by_url_id(id)

    return render_template(
        'urls/show.html',
        url=url,
        checks=checks,
        messages=messages,
        alert_classes=ALERT_CLASSES,
    )


@bp.post('/urls')
def urls_post():
    url_repo = current_app.url_repo

    form_data = request.form.to_dict()
    url = get_site_name(form_data['url'])

    errors = validate(url)
    if errors:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=url,
            messages=messages,
            alert_classes=ALERT_CLASSES,
        ), 422

    existing_url = url_repo.find_by_url(url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls.urls_show', id=existing_url['id']))

    form_data['url'] = url
    url_id = url_repo.save(form_data)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls.urls_show', id=url_id))


@bp.post('/urls/<id>/checks')
def urls_check(id):
    url_repo = current_app.url_repo
    url_check_repo = current_app.url_check_repo

    saved_url = url_repo.find(id).get('url')

    check_result = parse(saved_url)
    if 'error' in check_result:
        flash(
            check_result.get('error'), 'danger'
        )
    else:
        check_data = {
            'url_id': id,
        }
        check_data.update(check_result)
        url_check_repo.save(check_data)
        flash('Страница успешно проверена', 'success')

    return redirect(url_for('urls.urls_show', id=id))
