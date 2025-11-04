from flask import Flask
from os import getenv
from dotenv import load_dotenv
from page_analyzer.repository import UrlRepository, UrlCheckRepository

load_dotenv()


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['DATABASE_URL'] = getenv('DATABASE_URL')

    app.url_repo = UrlRepository(app.config['DATABASE_URL'])
    app.url_check_repo = UrlCheckRepository(app.config['DATABASE_URL'])

    from page_analyzer.main import bp as main_bp
    app.register_blueprint(main_bp)

    from page_analyzer.urls import bp as urls_bp
    app.register_blueprint(urls_bp)

    return app


app = create_app()
