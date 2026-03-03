from flask import Blueprint, jsonify, send_file, request
from server.config import MOD_LOADER_PATH
from json import load
from .utils import check_remote_ip, check_upload_file, check_form_data, get_file_path
from server.database import DBConnection
from server.database.schemas import ModsTable

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
@api_bp.route('/info/mods', methods=['GET'])
def get_mod_list():
    '''Send json display info about the currently installed mods'''
    
    with DBConnection() as db:
        mods_info = db.select_mods_info()

    return jsonify(mods_info)

@api_bp.route('/info/mod/<int:mod_id>', methods=['GET'])
def get_mod_info(mod_id:int):
    print(f'{mod_id = }')






















@api_bp.route('/admin/add-mod', methods=['POST'])
def add_mod():
    if check_remote_ip(request.remote_addr):
        return jsonify({'error': "IP not authorized"}), 403
    
    str_values = check_form_data(request.form)

    file, filename, filehash = check_upload_file(request.files)

    params = (
        str_values[ModsTable.NAME],
        str_values[ModsTable.DESCRIPTION],
        str_values[ModsTable.VERSION],
        filename,
        filehash,
        str_values[ModsTable.LINK],
        str_values[ModsTable.TYPE],
        str_values[ModsTable.ROLE]
    )

    with DBConnection() as db:
        db.insert_mod(params)

    save_path = get_file_path(filename, str_values[ModsTable.ROLE])
    file.save(save_path)

    return jsonify({"message": "Mod added successfully"}), 200
