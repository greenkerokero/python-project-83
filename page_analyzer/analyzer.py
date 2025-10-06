from flask import Flask
from dotenv import load_dotenv
from os import getenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'
