from flask import Flask
from os import getenv
from dotenv import load_dotenv
from .routes import init_routes


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

load_dotenv()
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['DATABASE_URL'] = getenv('DATABASE_URL')

init_routes(app)
