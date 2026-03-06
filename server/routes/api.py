#################################################################
# Python Lib Imports 

from flask import Blueprint, jsonify, send_file, request


#################################################################
# Server Imports

from server.database import DBConnection, ModsTable, DepsTable


#################################################################
# Local Imports


#################################################################
# Blueprint Object 

api_bp = Blueprint('api', __name__)


#################################################################
# API Info Routes

@api_bp.route('/info/modlist', methods=['GET'])
def get_mod_list():
    '''
    Return a list of all mods in the 'Mods' table as well as a list of dependencies

    Data is returned in the following format::

        [
            {
                "id": int,
                "name": str,
                "description": str,
                "version": str,
                "filename": str,
                "filehash": str,
                "link": str,
                "type": str,
                "role": str
                "dependencies": [str, ...]
            }, ...
        ]
    '''
    # open connection to database 
    with DBConnection() as db:
        # select full list of mods in the database
        modList = db.select_all_mods()

        # loop through each mod
        for mod in modList:
            # get the list of dependencies of the mod
            mod[DepsTable.TABLE_NAME.lower()] = db.select_mod_dependencies(int(mod[ModsTable.ID]))

    # return as json list of mods
    return jsonify(modList)


@api_bp.route('/info/mod/<int:modId>', methods=['GET'])
def get_mod_info(modId: int):
    '''
    Return mod from database given the id of that mod

    Data is returned in the following format::

        {
            "id": int,
            "name": str,
            "description": str,
            "version": str,
            "filename": str,
            "filehash": str,
            "link": str,
            "type": str,
            "role": str
            "dependencies": [str, ...]
        }
    '''
    # open connection to database
    with DBConnection() as db:
        # select mod based on ID
        modInfo = db.select_single_mod(modId)

        # get the list of dependencies of the mod
        modInfo[DepsTable.TABLE_NAME.lower()] = db.select_mod_dependencies(int(modInfo[ModsTable.ID]))

    # check if row exists
    if not modInfo:
        return jsonify({'error': f'{modId} is not an ID contained in the database'})

    # return json dictionary of columns mapping to their values
    return jsonify(modInfo)


@api_bp.route('/info/check-client', methods=['POST'])
def check_client_mods():
    '''
    Check the mods on the client side and determine which need to be downloaded and deleted

    POST request must be a json dictionary of filenames mapped to their filehash

    Example = {filename_1: filehash_1, ...}    

    Returns a dictionary that maps three lists to 'download', 'delete', and 'current'

    Data is returned in the following format::

        {
            "download": [filename_1, ...],
            "delete": [filename_1, ...],
            "current": [filename_1, ...]
        }
    '''
    # check that json is given
    if not request.is_json:
        return jsonify({'error': 'request payload must be json'})
    
    # attempt to get json from the incoming request
    data: dict|None = request.get_json(silent=True)

    # check that data given is valid json
    if data is None:
        return jsonify({'error': 'Unable to parse payload into json'})
    
    # convert dictionary of filenames -> filehash into a list of tuples (filenames, filehash)
    client_mods = [(k, v) for k, v in data.items()]

    # open connection to database and create temporary table
    with DBConnection(tempTable=True) as db:
        # insert client mods into the temp table
        db.insert_client_mods(client_mods)

        # get list of mods that client needs to download
        downloadList = db.select_client_downloads()

        # get list of mods that client needs to delete
        deleteList = db.select_client_deletes()

        # get list of mods that are current with the server
        currentList = db.select_client_current()

    # return as json dictionary of the three lists
    return jsonify({'download': downloadList, 'delete': deleteList, 'current': currentList})


#################################################################
# API Admin Routes


@api_bp.route('/admin/add/mod', methods=['POST'])
def add_mod():
    pass

















