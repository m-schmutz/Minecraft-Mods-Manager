#################################################################
# Python Lib Imports 

from flask import Blueprint, jsonify, send_file, request
from werkzeug.utils import secure_filename
from zipfile import ZipFile, is_zipfile
from json import load
from shutil import copyfileobj
from os import remove


#################################################################
# Server Imports

from lib.server.database import DBConnection, ModsTable, DepsTable


#################################################################
# Local Imports

from .utils import get_mod_filepath, check_file_name, verify_jar_file


#################################################################
# Blueprint Object 

api_bp = Blueprint('api', __name__)


#################################################################
# Constants

JAR_EXTENSION = '.jar'

JSON_EXTENSION = '.json'

ZIP_EXTENSION = '.zip'


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


@api_bp.route('/info/mod/<id>', methods=['GET'])
def get_mod_info(id: str):
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

    # attempt to convert URL parameter to an int
    try:
        modId = int(id)

    # return error if the parameter cannot be converted to an int
    except ValueError:
        return jsonify({'error': f'\'{id}\' is not a valid integer'})

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
# API Download Routes

@api_bp.route('/download/mod/<filename>', methods=['GET'])
def send_mod_file(filename: str):
    '''
    Return mod file for download given the mod filename
    '''
    # ensure that the filename passed is safe
    filename = secure_filename(filename)
    
    # open connection to database
    with DBConnection() as db:
        # search the database by filename to find role
        role = db.select_mod_role(filename)

    # check if a role was returned
    if not role:
        # return error json if filename could not be found in the database
        return jsonify({'error': f'\'{filename}\' does not match any filenames in the database'})

    # build filepath from the filename and the role
    filepath = get_mod_filepath(filename, role)

    # send the file that is located using the derived path
    return send_file(filepath, as_attachment=True)


@api_bp.route('/download/mods', methods=['POST'])
def send_mod_files():
    return jsonify({'error': 'not implemented yet'})


#################################################################
# API Admin Routes

@api_bp.route('/admin/upload/mod', methods=['POST'])
def upload_mod():
    '''
    Upload single mod file to the server

    Request must send the following data:
    
    - a file mapped to the key :\'mod-file\'

    - a json dictionary with the following keys defined: 

        - name: Display name of the mod file
        - description: Description of what the mod does
        - version: Display name for the version of the mod
        - link: Link to the curseforge page for the mod
        - type: The mod type (either 'Feature' or 'Library') 
        - role: Where the mod needs to be present (either 'Client/Server', 'Server', 'Client')
    '''
    try: 
        # get filestorage from form
        fileStorage = request.files.get('mod-file')

        # ensure that file was found
        if not fileStorage:
            raise ValueError('mod file must be mapped to key \'mod-file\'')

        # check that filename is valid
        safeFilename = check_file_name(fileStorage.filename, JAR_EXTENSION)

        # calculate hash
        filehash = verify_jar_file(fileStorage.stream, safeFilename)

        # put insert parameters into tuple
        params = (
            request.form.get(ModsTable.NAME),
            request.form.get(ModsTable.DESCRIPTION),
            request.form.get(ModsTable.VERSION),
            safeFilename,
            filehash,
            request.form.get(ModsTable.LINK),
            request.form.get(ModsTable.TYPE),
            request.form.get(ModsTable.ROLE)
        )

        # insert mod into the database
        with DBConnection() as db:
            db.insert_mod(params)

        # save the mod file to either the server mods directory or the client mods directory
        savePath = get_mod_filepath(safeFilename, request.form.get(ModsTable.ROLE))
        fileStorage.save(savePath)

        # return success
        return jsonify({'success': f'{safeFilename} uploaded to database'})
    
    # return error
    except Exception as e:
        return jsonify({'error': str(e)})


@api_bp.route('/admin/upload/mods', methods=['POST'])
def upload_mods():
    try: 
        zipFile = request.files.get('mods-zip')
        manifestFile = request.files.get('manifest')

        if not zipFile:
            raise ValueError('zip file of mods must be mapped to key \'mods-zip\'')

        if not manifestFile:
            raise ValueError('manifest json file must be mapped to key \'manifest\'')

        manifest: dict[str, dict[str, str]] = load(manifestFile.stream)

        savepaths = list()

        with ZipFile(zipFile.stream) as z:
            if not set(manifest.keys()) == set(z.namelist()):
                raise ValueError('filenames in manifest file do not match filenames in zip file')
            
            with DBConnection() as db:
                for zFile in z.infolist():

                    metadata = manifest[zFile.filename]
                
                for rawFilename, metadata in manifest.items():
                    with z.open(rawFilename) as zf:

                        safeFilename = check_file_name(rawFilename, JAR_EXTENSION)

                        filehash = verify_jar_file(zf, safeFilename)

                        params = (
                            metadata.get(ModsTable.NAME),
                            metadata.get(ModsTable.DESCRIPTION),
                            metadata.get(ModsTable.VERSION),
                            safeFilename,
                            filehash,
                            metadata.get(ModsTable.LINK),
                            metadata.get(ModsTable.TYPE),
                            metadata.get(ModsTable.ROLE)
                        )

                        db.insert_mod(params)

                        savePath = get_mod_filepath(safeFilename, metadata.get(ModsTable.ROLE))

                        with open(savePath, 'wb') as f:
                            copyfileobj(zf, f)
                        
                        savepaths.append(savePath)

        return jsonify({'success': f'added {len(savepaths)} mods'})


    except Exception as e:

        for path in savepaths:
            remove(path)

        return jsonify({'error': f'{type(e)}: {str(e)}'})
