from flask import Blueprint, jsonify, send_file, request
from server.config import MOD_LOADER_PATH
from json import load
from .utils import check_remote_ip, check_upload_file, check_form_data, get_file_path
from server.database.params import ModInsert
from server.database.db import DBConnection


# api blueprint
api_bp = Blueprint('api', __name__)


### API DOWNLOAD ROUTES ###


# route for sending the mod loader installer to the user
@api_bp.route('/download/mod-loader', methods=['GET'])
def send_mod_loader():
    '''Send the mod loader file to the client'''
    return send_file(MOD_LOADER_PATH, as_attachment=True)


### API INFO ROUTES ###


# route for returning the server mod list
@api_bp.route('/info/mod-display-list', methods=['GET'])
def get_mod_list():
    '''Send json display info about the currently installed mods'''
    with open('/home/msch/Projects/Minecraft-Mods-Manager/mod-list.json', 'r') as f:
        data = load(f)
    return jsonify(data)


@api_bp.route('/admin/add-mod', methods=['POST'])
def add_mod():
    if check_remote_ip(request.remote_addr):
        return jsonify({'error': "IP not authorized"}), 403
    

    str_values = check_form_data(request.form)

    file, filename, filehash = check_upload_file(request.files)

    new_mod = ModInsert(str_values, filename, filehash)

    with DBConnection() as db:
        db.add_mod(new_mod)

    save_path = get_file_path(filename, new_mod.role)
    file.save(save_path)

    return jsonify({"message": "Mod added successfully"}), 200