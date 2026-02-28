from hashlib import file_digest, sha256
from server.config import ADMIN_IPS, SERVER_MODS_DIR, CLIENT_MODS_DIR
from typing import BinaryIO
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from werkzeug.utils import secure_filename
from server.database.schemas import ModsTable, TypeValues, RoleValues
from os.path import join


FORM_STR_KEYS = [
    ModsTable.NAME, 
    ModsTable.DESCRIPTION,
    ModsTable.VERSION,
    ModsTable.LINK,
]

VALID_TYPE_VALUES = {TypeValues.FEATURE, TypeValues.LIBRARY}

VALID_ROLE_VALUES = {RoleValues.BOTH, RoleValues.SERVER, RoleValues.CLIENT}


def calc_hash(stream: BinaryIO) -> str:
    '''Hash the contents of a file and return its hex digest using HASH_FUNCTION'''
    # calculate hash
    digest = file_digest(stream, sha256)
    
    # reset to begin of file
    stream.seek(0)

    # return as a hex digest
    return digest.hexdigest()


def check_remote_ip(remote_ip:str) -> str:
    '''Return True if remote IP is not in ADMIN_IPS'''
    return remote_ip not in ADMIN_IPS


def check_upload_file(filesContainer: ImmutableMultiDict[str, FileStorage]) -> tuple[FileStorage, str, str]:
    
    files = filesContainer.getlist('file_upload')
    
    if (len(files) == 0):
        raise ValueError('No File Uploaded')
    
    if (len(files) > 1):
        raise ValueError('Only one file per upload allowed')
    
    file = files[0]

    if not file.filename.endswith('.jar'):
        raise ValueError('Only .jar files are allowed')
    
    if ' ' in file.filename:
        raise ValueError('Filename cannot have any spaces')

    filehash = calc_hash(file.stream)
    
    return file, secure_filename(file.filename), filehash


def check_form_data(formData: ImmutableMultiDict[str, str]) -> dict[str, str]:
    
    for k in FORM_STR_KEYS:
        if formData[k] is None:
            raise ValueError(f'No string provided for {k}')

    if formData[ModsTable.TYPE] not in VALID_TYPE_VALUES:
        raise ValueError(f'{ModsTable.TYPE} value must be in {VALID_TYPE_VALUES}')
    
    if formData[ModsTable.ROLE] not in VALID_ROLE_VALUES:
        raise ValueError(f'{ModsTable.ROLE} value must be in {VALID_ROLE_VALUES}')
    
    return formData.to_dict(flat=True)
        

def get_file_path(filename: str, role: str):
    if role == RoleValues.BOTH or role == RoleValues.SERVER:
        return join(SERVER_MODS_DIR, filename)

    elif role == RoleValues.CLIENT:
        return join(CLIENT_MODS_DIR, filename)
    
    else:
        raise ValueError(f'Unable to get path, \'{role}\' is not a valid role')