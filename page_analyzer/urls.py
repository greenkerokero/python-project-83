from uuid import uuid4

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.parser import parse
from page_analyzer.url_service import (
    datatime_formater,
    get_site_name,
    validate,
)

bp = Blueprint('urls', __name__)

ALERT_CLASSES = {
    'success': 'success',
    'info': 'info',
    'danger': 'danger'
}


@bp.route('/urls')
def urls_get():
    url_value_repo = current_app.url_value_repo
    urls = url_value_repo.get_last_check_data()

    formated_urls = []

    for url in urls:
        url['created_at'] = datatime_formater(url.get('created_at'))

        if not url.get('status_code'):
            url['status_code'] = ''

        formated_urls.append(url)

    return render_template(
        'urls/index.html',
        urls=formated_urls,
    )


@bp.route('/urls/<id>')
def urls_show(id):
    url_repo = current_app.url_repo
    url_check_repo = current_app.url_check_repo

    messages = get_flashed_messages(with_categories=True)
    url = url_repo.find(id)

    if url is None:
        abort(404)

    url['created_at'] = datatime_formater(url.get('created_at'))

    checks = url_check_repo.find_by_url_id(id)

    return render_template(
        'urls/show.html',
        url=url,
        checks=checks,
        messages=messages,
        alert_classes=ALERT_CLASSES,
    )


@bp.route('/urls', methods=['POST'])
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


@bp.route('/urls/<id>/checks', methods=['POST'])
def urls_check(id):
    url_repo = current_app.url_repo
    url_check_repo = current_app.url_check_repo

    url_data = url_repo.find(id)
    saved_url = url_data.get('url')

    if not saved_url:
        flash('Произошла ошибка при проверке', 'danger')
        operation_id = str(uuid4())
        current_app.logger.warning(
            f'[Operation ID: {operation_id}] Передан пустой URL'
        )
        return redirect(url_for('urls.urls_show', id=id))

    check_result = parse(saved_url)
    if 'error' in check_result:
        flash('Произошла ошибка при проверке', 'danger')
        operation_id = str(uuid4())
        current_app.logger.warning(
            f'[Operation ID: {operation_id}] '
            f'Не удалось проверить {saved_url}: {check_result.get('error')}'
        )
    else:
        check_data = {
            'url_id': id,
        }
        check_data.update(check_result)
        url_check_repo.save(check_data)
        flash('Страница успешно проверена', 'success')

    return redirect(url_for('urls.urls_show', id=id))
