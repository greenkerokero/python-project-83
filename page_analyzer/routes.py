from flask import render_template


def init_routes(app):
    @app.get('/')
    def index():
        return render_template(
            'index.html'
        )
