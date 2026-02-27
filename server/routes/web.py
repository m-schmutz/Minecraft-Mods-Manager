from flask import Blueprint, render_template, redirect, request
from .utils import check_remote_ip
from server.config import MC_MODLOADER, MC_VERSION, MC_DIFFICULTY
from server.database.schemas import RoleValues, TypeValues, ModsTable


# web related blueprints
web_bp = Blueprint('web', __name__)


# route for redirecting root path to home page
@web_bp.route('/', methods=['GET'])
def root_page():
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


### API ADMIN ROUTES ###


# route for admin page
@web_bp.route('/admin', methods=['GET'])
def admin_page():
    if check_remote_ip(request.remote_addr):
        return render_template('403.html'), 403
    return render_template('admin.html')


# route for add-mod page
@web_bp.route('/admin/add-mod', methods=['GET'])
def add_mod_page():
    if check_remote_ip(request.remote_addr):
        return render_template('403.html'), 403
    return render_template(
        'add-mod.html',
        name_col=ModsTable.DISPLAY_NAME,
        desc_col=ModsTable.DESCRIPTION,
        version_col=ModsTable.VERSION,
        link_col=ModsTable.LINK,
        type_col=ModsTable.MOD_TYPE,
        role_col=ModsTable.MOD_ROLE,
        file_col=ModsTable.MOD_FILE,
        types=[TypeValues.FEATURE, TypeValues.LIBRARY],
        roles=[RoleValues.BOTH, RoleValues.CLIENT, RoleValues.SERVER]
    )