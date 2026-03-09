#################################################################
# Python Lib Imports 

from os.path import isfile, isdir, isabs


#################################################################
# Server Configuration
#
# SERVER_MODS_DIR: Directory that server mods are stored in. For production this should be the 'mods' folder for the server. 
# 
# CLIENT_MODS_DIR: Directory that is used for storing client-side only mods.
#
# DB_PATH: Absolute path to the file that sqlite should use to store the database
#
# MOD_LOADER_PATH: Absolute path to the .jar installer file for the Mod Loader
#
# ADMIN_IP: Set of IP's that are allowed to access the 'admin' routes of the website and api (modifying mod files)
#
# MC_VERSION: Display name for the version of minecraft that the server is using 
#
# MC_DIFFICULTY: Display name for the difficulty that the minecraft server is set to
#
# MC_MODLOADER: Display name for the Mod Loader used for the minecraft server
#
#
#################################################################
# SERVER DIRECTORY PATHS (REQUIRED)

# mods directory for the server 
SERVER_MODS_DIR = ''

# directory for holding client-specific mods
CLIENT_MODS_DIR = ''


#################################################################
# SERVER FILE PATHS (REQUIRED)

# path to where sqlite database file should be located
DB_PATH = ''

# path to minecraft installer
MOD_LOADER_PATH = ''


#################################################################
# ADMIN IPS 

# IP's allowed to access admin routes (localhost and my VPN IP)
ADMIN_IPS = {'127.0.0.1'}


#################################################################
# DISPLAY NAMES

# Minecraft server version
MC_VERSION = ''

# Minecraft server difficulty
MC_DIFFICULTY = ''

# Minecraft mod loader
MC_MODLOADER = ''


#################################################################
# SERVER CONFIG CHECK FUNCTION

def check_config():
    # check that directory paths are valid
    for dirPath in [SERVER_MODS_DIR, CLIENT_MODS_DIR]:
        if not isdir(dirPath):
            raise ValueError(f'\'{dirPath}\' is not a valid directory path')
        
        elif not isabs(dirPath):
            raise ValueError(f'\'{dirPath}\' is not an absolute path')
        
    # check that file paths are valid
    for filePath in [DB_PATH, MOD_LOADER_PATH]:
        if not isfile(filePath):
            raise ValueError(f'\'{filePath}\' is not a valid file path')
        
        elif not isabs(dirPath):
            raise ValueError(f'\'{dirPath}\' is not an absolute path')
        
    # check if admin ip's are defined
    if len(ADMIN_IPS) == 0:
        print('WARNING: NO IP\'s defined to access \'admin\' routes')
        
    # check if version is defined
    if MC_VERSION is None:
        print('WARNING: No display name for minecraft server')

    # check if difficulty is defined
    if MC_DIFFICULTY is None:
        print('WARNING: No display name for minecraft difficulty')
    
    # check if mod loader is defined
    if MC_MODLOADER is None:
        print('WARNING: No display name for minecraft server mod loader')
