############ SERVER DIRECTORY PATHS ############


# mods directory for the server 
SERVER_MODS_DIR = None

# directory for holding client-specific mods
CLIENT_MODS_DIR = None

# directory for holding temp files
TEMP_DIR = None


############ SERVER FILEPATHS (MUST BE ABSOLUTE) ############


# path to where sqlite database file should be located
DB_PATH = None

# path to minecraft installer
MOD_LOADER_PATH = None


############ SERVER CONSTANTS ############


# IP's allowed to access admin routes (localhost and my VPN IP)
ADMIN_IPS = {"127.0.0.1", "172.30.1.10"}
# ADMIN_IPS = {}

# Minecraft server version
MC_VERSION = None

# Minecraft server difficulty
MC_DIFFICULTY = None

# Minecraft mod loader
MC_MODLOADER = None


############ SERVER CONFIG CHECK FUNCTION ############


def check_config():
    pass