#################################################################
# Python Lib Imports

from flask import Blueprint, render_template, redirect, request


#################################################################
# Server Imports

from lib.server.database.schemas import RoleValues, TypeValues
from lib.server.config import MC_MODLOADER, MC_VERSION, MC_DIFFICULTY


#################################################################
# Local Imports



#################################################################
# Blueprint Object

# web related blueprint
web_bp = Blueprint('web', __name__)


#################################################################
# Web Routes

# route for redirecting root path to home page
@web_bp.route('/', methods=['GET'])
def home_redirect():
    return redirect('/home')


# route for serving the home page
@web_bp.route('/home', methods=['GET'])
def home_page():
    return render_template(
        'home.html',
        mc_modloader=MC_MODLOADER,
        mc_version=MC_VERSION,
        mc_difficulty=MC_DIFFICULTY,
        roles=['All', RoleValues.BOTH, RoleValues.CLIENT, RoleValues.SERVER],
        types=['All', TypeValues.FEATURE, TypeValues.LIBRARY]
    )


