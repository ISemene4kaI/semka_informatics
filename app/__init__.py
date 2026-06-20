from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from app.routes.files import files_bp
from app.routes.health import health_bp
from app.routes.pages import pages_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
    )

    app.register_blueprint(pages_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(health_bp)

    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(413)
    @app.errorhandler(500)
    def render_error(error):
        return render_template("error.html", error=error), error.code

    return app
