from flask import Flask
from os import getenv, path, mkdir, getpid
from dotenv import load_dotenv
from logging import Formatter, INFO
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid4
from page_analyzer.repository import (
    UrlRepository,
    UrlCheckRepository,
    UrlViewRepository,
)

load_dotenv()


def create_app():
    LOGS_DIR = 'logs'
    worker_id = getpid()
    operation_id = str(uuid4())

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['DATABASE_URL'] = getenv('DATABASE_URL')

    app.url_repo = UrlRepository(app.config['DATABASE_URL'])
    app.url_check_repo = UrlCheckRepository(app.config['DATABASE_URL'])
    app.url_value_repo = UrlViewRepository(app.config['DATABASE_URL'])

    from page_analyzer.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from page_analyzer.main import bp as main_bp
    app.register_blueprint(main_bp)

    from page_analyzer.urls import bp as urls_bp
    app.register_blueprint(urls_bp)

    if not path.exists(LOGS_DIR):
        mkdir(LOGS_DIR)
    file_handler = TimedRotatingFileHandler(
        filename=f'{LOGS_DIR}/app.log',
        when='W0',
        interval=1,
        backupCount=4,
        encoding='utf-8'
    )
    file_handler.setFormatter(Formatter(
        f'%(asctime)s %(levelname)s: [Worker ID: {worker_id}] %(message)s'))
    file_handler.setLevel(INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(INFO)
    app.logger.info(f'[Operation ID: {operation_id}] Page analyzer startup')

    return app


app = create_app()
