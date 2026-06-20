from flask import Flask

from routes.pages import pages_bp
from routes.files import files_bp
from routes.health import health_bp


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(pages_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(health_bp)

    return app
