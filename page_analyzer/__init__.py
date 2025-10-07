from flask import Flask
from . import routes
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
