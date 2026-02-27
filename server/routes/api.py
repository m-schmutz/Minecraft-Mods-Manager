from flask import Blueprint, jsonify, send_file, request
from server.config import MOD_LOADER_PATH
from json import load
from .utils import check_remote_ip


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

