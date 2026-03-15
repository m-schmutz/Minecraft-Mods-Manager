#################################################################
# Python Lib Imports 

from flask import Flask
from sys import exit


#################################################################
# Local Imports 

from .config import check_config
from .routes import api_bp


#################################################################
# create_app function

def create_app() -> Flask:
    '''Create flask app using web and api blueprints'''
    # check that config is valid
    try:
        check_config()

    # exit on config error
    except ValueError as e:
        print('CONFIG ERROR: Check config file located at lib/server/config.py')
        print(f'\t-> {e}')
        exit(1)

    # create Flask app object
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # register blueprints
    # app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # return Flask app object
    return app