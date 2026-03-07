#################################################################
# Python Lib Imports 

from os.path import join


#################################################################
# Server Imports 

from server.database.schemas import RoleValues
from server.config import SERVER_MODS_DIR, CLIENT_MODS_DIR


#################################################################
# Routes Utility Functions 

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
