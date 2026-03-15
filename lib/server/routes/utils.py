#################################################################
# Python Lib Imports 

from os.path import join
from hashlib import file_digest, sha256
from typing import BinaryIO
from werkzeug.utils import secure_filename
from zipfile import ZipFile, is_zipfile


#################################################################
# Server Imports 

from lib.server.database.schemas import RoleValues
from lib.server.config import SERVER_MODS_DIR, CLIENT_MODS_DIR, ADMIN_IPS


#################################################################
# Constants

JAR_MANIFEST = 'META-INF/MANIFEST.MF'


#################################################################
# Internal Functions 

def _calc_hash(stream: BinaryIO) -> str:
    '''
    Hash the contents of a file and return its hex digest using HASH_FUNCTION
    '''
    # calculate hash
    digest = file_digest(stream, sha256)
    
    # reset to begin of file
    stream.seek(0)

    # return as a hex digest
    return digest.hexdigest()


def _find_manifest(zip: ZipFile):
    '''
    Check if the opened zipfile contains a 'MANIFEST.MF' file present in mod files
    '''
    try:
        # attempt to get file
        zip.getinfo(JAR_MANIFEST)

        # return true if found
        return True
    
    # otherwise return false
    except KeyError:
        return False


#################################################################
# Routes Utility Functions 

def check_remote_ip(remote_ip:str) -> bool:
    '''
    Return True if remote IP is not in ADMIN_IPS
    '''
    return remote_ip not in ADMIN_IPS


def get_mod_filepath(filename: str, role: str):
    '''
    Return the path to the mod file based on its role
    '''
    # check if the role is client
    if role == RoleValues.CLIENT:
        # return the full path to the mod file in the client folder
        return join(CLIENT_MODS_DIR, filename)

    # return full path to the mod file in the server folder
    return join(SERVER_MODS_DIR, filename)


def check_file_name(filename: str, ext: str):
    
    # ensure that filename is safe
    safeFilename = secure_filename(filename)

    # check that a secure filename could be made
    if not safeFilename:
        raise ValueError('filename is invalid')

    # check that filename has correct extension
    if not safeFilename.endswith(ext):
        raise ValueError(f'File must have \'{ext}\' extension')
    
    # return the filename as a safe version (no spaces and not directory escapes)
    return safeFilename


def verify_jar_file(fileContents: BinaryIO, filename: str):
    # check that the file has the correct signature
    if not is_zipfile(fileContents):
        raise ValueError('File is not a valid jar file')
    
    # open jar file as zip
    with ZipFile(fileContents, 'r') as z:
        # check if file is corrupted
        if z.testzip():
            raise ValueError(f'{filename} is corrupted')
        
        # check if manifest is in the jar file
        if not _find_manifest(z):
            raise ValueError(f'{filename} is not a valid mod file, no manifest could be found')
        
    # return sha256 hash of file contents
    return _calc_hash(fileContents)
