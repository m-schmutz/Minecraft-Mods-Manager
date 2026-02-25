try:
    import os
    import signal
    import zipfile
    import requests
    import shutil
    import hashlib
    import json
    import argparse
    import shutil
except ModuleNotFoundError as e:
    print("Python module not installed:", e)
    quit()



### CONSTANTS ###

FILE_SERVER_ADDR = "http://172.30.1.1:8000/files/"
MOD_PACK_ENDPOINT       = "ModPack.zip"
SHADER_PACK_ENDPOINT    = "BSL_v10.1.zip"
NEOFORGE_ENDPOINT       = "neoforge-21.1.218-installer.jar"

OUTPUT_DIR_ABSPATH: str
CURRENT_DIR_ABSPATH: str
DOWNLOADS_DIR_ABSPATH: str



### UTILS ###

class QuitException(Exception):
    """So you want to quit the program, eh?"""
    def __init__(self, *args):
        super().__init__(*args)

def raise_quit_exception(*args, **kwargs):
    """This takes any args to appease signal handling btw"""
    raise QuitException()


def ask_user(query: str,
             valid_responses: tuple[str] | None = None,
             *,
             show_responses: bool = True,
             case_sensitive: bool = False,
             responses_delimeter: str = ","):
    if not isinstance(query ,str):
        raise TypeError("query must be a string")
    
    if not isinstance(show_responses, bool):
        raise TypeError("show_responses must be a boolean")
    
    if not isinstance(case_sensitive, bool):
        raise TypeError("case_sensitive must be a boolean")

    if not isinstance(responses_delimeter ,str):
        raise TypeError("response_delimeter must be a string")


    resp = None
    if valid_responses is None:    
        resp = input(query)
    else:
        for vr in valid_responses:
            if not isinstance(vr, str):
                raise TypeError("All responses must be strings")
        
        if show_responses:
            query += f" ({responses_delimeter.join(valid_responses)}): "

        if not case_sensitive:
            valid_responses = tuple(vr.lower() for vr in valid_responses)

        while resp not in valid_responses:
            resp = input(query)
            if not case_sensitive:
                resp = resp.lower()
    
    return resp

def ask_user_yes_no(query: str, **kwargs):
    return ask_user(query, ("y","n"), **kwargs)

def ask_user_replace_file(path: str):
    if os.path.exists(path):
        if "n" == ask_user_yes_no(f"File \"{os.path.relpath(path)}\" already exists. Would you like to replace it?"):
            return False
    return True


def get_minecraft_dir():
    dot_minecraft_dir_abspath = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft")
    if not os.path.exists(dot_minecraft_dir_abspath):
        raise Exception("Could not locate .minecraft directory")
    return dot_minecraft_dir_abspath

def download_file(url: str, filename: str):
    global DOWNLOADS_DIR_ABSPATH    
    dest_abspath = os.path.join(DOWNLOADS_DIR_ABSPATH, filename)

    if ask_user_replace_file(dest_abspath):
        did_timeout = False

        print("Downloading", url)
        try:
            resp = requests.get(url, timeout=10)
        except requests.ConnectTimeout:
            did_timeout = True
        
        if did_timeout:
            raise Exception("Timeout. Is your VPN connected?")
        elif resp.status_code != 200:
            raise Exception(f"Failed to download {url} ({resp.status_code}, {resp.reason})")
        
        with open(dest_abspath, "wb") as file:
            file.write(resp.content)
    
        print("Successfully downloaded", os.path.relpath(dest_abspath))
    
    return dest_abspath

def zip_dir(src_dir: str, dst_dir: str):
    if not isinstance(src_dir, str):
        raise TypeError("src_dir must be a str")
    
    if not isinstance(dst_dir, str):
        raise TypeError("dst_dir must be a str")
    

    # Make paths absolute
    if os.path.isdir(src_dir):
        src_dir = os.path.abspath(src_dir)
    else:
        raise NotADirectoryError(src_dir)
    
    if os.path.isdir(dst_dir):
        dst_dir = os.path.abspath(dst_dir)
    else:
        raise NotADirectoryError(dst_dir)
    

    zip_filename = os.path.basename(src_dir) + ".zip"
    output_file_abspath = os.path.join(dst_dir, zip_filename)
    mod_filenames = tuple(f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f)))
    
    print(f"Zipping mods ({len(mod_filenames)})...")    
    with zipfile.ZipFile(output_file_abspath, "w") as zip:
        for file in mod_filenames:
            abspath = os.path.join(src_dir, file)
            print("  Adding", os.path.relpath(abspath))
            zip.write(abspath, file)
    
    return output_file_abspath



### PROGRAM ROUTINES ###

def setup():
    global CURRENT_DIR_ABSPATH
    global DOWNLOADS_DIR_ABSPATH
    global OUTPUT_DIR_ABSPATH


    # Quit gracefully on Ctrl+C
    signal.signal(signal.SIGINT, raise_quit_exception)


    # Move to directory which contains this file
    CURRENT_DIR_ABSPATH = os.path.abspath(os.path.dirname(__file__))
    if os.path.isdir(CURRENT_DIR_ABSPATH):
        os.chdir(CURRENT_DIR_ABSPATH)
    else:
        raise Exception("Cannot determine current path")


    # Create downloads directory
    DOWNLOADS_DIR_ABSPATH = os.path.abspath(os.path.join(".cache", "downloads"))
    if not os.path.exists(DOWNLOADS_DIR_ABSPATH):
        os.makedirs(DOWNLOADS_DIR_ABSPATH)
    
    # Create output directory
    OUTPUT_DIR_ABSPATH = os.path.abspath("output")
    if not os.path.exists(OUTPUT_DIR_ABSPATH):
        os.makedirs(OUTPUT_DIR_ABSPATH)


    init_mod_hash_table()

def init_mod_hash_table():
    global CURRENT_DIR_ABSPATH

    _FILE = os.path.join(CURRENT_DIR_ABSPATH, ".cache", "mod-hashes.json")

    table = dict()
    mods_dir = os.path.join(get_minecraft_dir(), "mods")

    if os.path.exists(_FILE):
        with open(_FILE) as file:
            table = json.load(file)
    else:
        print("Initializing mods hash table... ", end="", flush=True)
        for mod in (f for f in os.listdir(mods_dir) if os.path.isfile(os.path.join(mods_dir, f))):
            with open(os.path.join(mods_dir, mod), "rb") as file:
                table.update({mod: hashlib.sha256(file.read()).hexdigest()})
        
        with open(_FILE, "w") as file:
            file.write(json.dumps(table))
        print("Done")
    
    return table



def zip_mods(src_dir: str):
    global OUTPUT_DIR_ABSPATH
    
    # The directory containing all mods to zip
    src_dir = os.path.abspath(src_dir)
    if not os.path.isdir(src_dir):
        raise Exception(f"Directory does not exist: {os.path.relpath(src_dir)}")
    else:
        files = os.listdir(src_dir)
        if not files:
            raise Exception(f"Directory is empty: {os.path.relpath(src_dir)}")
        else:
            for file in files:
                if not file.endswith(".jar"):
                    raise Exception(f"All files in {os.path.relpath(src_dir)} must be a .jar")
    
    # The zipfile to create
    output_file_abspath = os.path.join(OUTPUT_DIR_ABSPATH, "mods.zip")
    if ask_user_replace_file(output_file_abspath):
        file = zip_dir(src_dir, OUTPUT_DIR_ABSPATH)
        print("Successfully created", os.path.relpath(file))

def update_client_mods():
    global MOD_PACK_ENDPOINT

    # Determine path to local .minecraft directory
    mods_dir_abspath = os.path.join(get_minecraft_dir(), "mods")

    # Download new mods
    new_mods_zip_abspath = download_file(FILE_SERVER_ADDR + MOD_PACK_ENDPOINT, "mods.zip")
    with zipfile.ZipFile(new_mods_zip_abspath) as zip:
        new_mod_filenames = set(entry.filename for entry in zip.infolist())

    # Gather existing mod names
    existing_mod_filenames = set(f for f in os.listdir(mods_dir_abspath) if os.path.isfile(os.path.join(mods_dir_abspath, f)))

    # If the user has mods which are not part of the new set, ask if they
    # are OK with them being deleted. They will be lost forever.
    existing_mod_filenames_lost = existing_mod_filenames - new_mod_filenames
    if existing_mod_filenames_lost:
        print("The following files will be deleted:")
        for m in sorted(existing_mod_filenames_lost):
            print(" ", m)

        if "n" == ask_user_yes_no("Continue?"):
            return
    
    # Remove existing mods
    for filename in existing_mod_filenames:
        os.remove(os.path.join(mods_dir_abspath, filename))
    
    # Extract new mods
    print(f"Updating mods ({len(new_mod_filenames)})...")
    with zipfile.ZipFile(new_mods_zip_abspath) as zip:
        for item in zip.infolist():
            print("  Installing", item.filename)
            zip.extract(item, mods_dir_abspath)
    print("Successfully updated mods")

    # Delete downloaded zip
    os.remove(new_mods_zip_abspath)

def update_client_shaders():
    global SHADER_PACK_ENDPOINT

    # Get path to local shaderpack dir
    shaderpacks_dir_abspath = os.path.join(get_minecraft_dir(), "shaderpacks")

    # Download shaderpack
    new_shaderpack_abspath = download_file(FILE_SERVER_ADDR + SHADER_PACK_ENDPOINT, SHADER_PACK_ENDPOINT)

    # Install/replace the shaderpack
    dest = os.path.join(shaderpacks_dir_abspath, SHADER_PACK_ENDPOINT)
    if os.path.exists(dest):
        if "n" == ask_user_replace_file(dest):
            return
    
    shutil.move(new_shaderpack_abspath, dest)
    
def clear_cache():
    downloads_dir = os.path.join(CURRENT_DIR_ABSPATH, ".cache")
    shutil.rmtree(downloads_dir)






### MAIN PROGRAM ###

def main():
    parser = argparse.ArgumentParser(prog=__file__.rsplit(os.sep, maxsplit=1)[-1],
                                     add_help=False,
                                     exit_on_error=False)
    parser.add_argument("-h", "--help",
                        action="store_true",
                        help="Show this message and exit.")
    parser.add_argument("-m", "--update-mods",
                        action="store_true",
                        help="Download and install latest mods.")
    parser.add_argument("-s", "--update-shaders",
                        action="store_true",
                        help="Download and install latest shaders.")
    parser.add_argument("--zip-mods",
                        nargs=1,
                        metavar="DIR",
                        help="Compress all mods in DIR to a zip file.")
    parser.add_argument("--clear-cache",
                        action="store_true",
                        help="Clear your local cache")
    
    try:
        args = vars(parser.parse_args())
        if not any(args.values()) or args["help"]:
            parser.print_help()
            return

        setup()

        # Run specified tasks then quit
        if args["update_mods"]:
            update_client_mods()
        if args["update_shaders"]:
            update_client_shaders()
        if args["zip_mods"]:
            zip_mods(*args["zip_mods"])
        if args["clear_cache"]:
            clear_cache()

    except argparse.ArgumentError as e:
        print(e)
        parser.print_usage()
    
    except QuitException:
        print("Quitting...")
    
    except Exception as e:
        print(f"\x1b[91m{e}\x1b[0m") # red message
        raise e

if __name__ == "__main__":
    main()
