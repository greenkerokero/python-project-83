from flask import (
    render_template,
)
from dotenv import load_dotenv
from os import getenv
from page_analyzer import app

load_dotenv()
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template(
        'index.html'
    )
