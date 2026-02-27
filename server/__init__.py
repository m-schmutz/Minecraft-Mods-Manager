from flask import Flask
from .config import check_config


def create_app() -> Flask:
    '''Create flask app using web and api blueprints'''
    # check that config is valid
    check_config()

    # create Flask app object
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # import route blueprints
    from .routes import api_bp, web_bp

    # register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # return Flask app object
    return app