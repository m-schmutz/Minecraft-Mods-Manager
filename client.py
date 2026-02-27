#################################################
# client.py
# 2026-02-25, Ryan Stachura
#
# Command line utility to manage local mods for
# self-hosted Minecraft server.
#################################################

try:
    import os
    import signal
    import zipfile
    import requests
    import shutil
    import hashlib
    import json
    import argparse
    from progress_bar import ProgressBar
except ModuleNotFoundError as e:
    print("Python module not installed:", e)
    quit()



### CONSTANTS & GLOBALS ###

FILE_SERVER_ADDR = "http://172.30.1.1:8000/files/"
MOD_PACK_ENDPOINT       = "ModPack.zip"
SHADER_PACK_ENDPOINT    = "BSL_v10.1.zip"
NEOFORGE_ENDPOINT       = "neoforge-21.1.218-installer.jar"

PATH_CACHE      = ".cache"
PATH_DOWNLOADS  = os.path.join(PATH_CACHE, "downloads")
PATH_MOD_HASHES = os.path.join(PATH_CACHE, "mod-hashes.json")

do_quit = False



### UTILS ###

class QuitProgram(Exception):
    """So you want to quit the program, eh?"""
    def __init__(self, *args):
        super().__init__(*args)

def signal_handler(*args, **kwargs):
    global do_quit
    do_quit = True


def red(s: str):
    return f"\x1b[91m{s}\x1b[0m"

def green(s: str):
    return f"\x1b[92m{s}\x1b[0m"

def yellow(s: str):
    return f"\x1b[93m{s}\x1b[0m"


def ask_user(query: str,
             valid_responses: tuple[str] | None = None,
             *,
             show_responses: bool = True,
             case_sensitive: bool = False,
             responses_delimeter: str = ","):
    global do_quit

    if not isinstance(query ,str):
        raise TypeError("query must be a string")
    
    if not isinstance(show_responses, bool):
        raise TypeError("show_responses must be a boolean")
    
    if not isinstance(case_sensitive, bool):
        raise TypeError("case_sensitive must be a boolean")

    if not isinstance(responses_delimeter ,str):
        raise TypeError("response_delimeter must be a string")


    # `input()` will throw an empty exception if SIGINT is caught by caller.
    # This is because when SIGINT is caught by the caller, it prevents the
    # default behavior of raising KeyboardInterrupt.
    #
    # Therefore, we use try-except blocks then check that our signal handler
    # was called.
    def _try_input(q) -> str:
        global do_quit
        try:
            return input(q)
        except Exception:
            if do_quit:
                raise QuitProgram()


    resp = ""
    if valid_responses is None:    
        resp = _try_input(query)
    else:
        for vr in valid_responses:
            if not isinstance(vr, str):
                raise TypeError("All responses must be strings")
        
        if show_responses:
            query += f" ({responses_delimeter.join(valid_responses)}): "

        if not case_sensitive:
            valid_responses = tuple(vr.lower() for vr in valid_responses)

        while resp not in valid_responses:
            resp = _try_input(query)
            if not case_sensitive:
                resp = resp.lower()
    
    return resp

def ask_user_yes_no(query: str, **kwargs):
    return "y" == ask_user(query, ("y","n"), **kwargs)

def ask_user_replace_file(path: str):
    if os.path.exists(path):
        return ask_user_yes_no(f"File \"{os.path.relpath(path)}\" already exists. Would you like to replace it?")
    return True


def get_minecraft_dir():
    dot_minecraft_dir_abspath = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft")
    if not os.path.exists(dot_minecraft_dir_abspath):
        raise Exception("Could not locate .minecraft directory")
    return dot_minecraft_dir_abspath

def download_file(url: str, filename: str):
    global do_quit

    chunk_size = 4096
    dest = os.path.join(PATH_DOWNLOADS, filename)

    if ask_user_replace_file(dest):
        print(f"Downloading {url}...")
        try:
            with requests.get(url, timeout=5.0, stream=True) as resp_stream:
                if resp_stream.status_code != 200:
                    raise Exception(f"Failed ({resp_stream.status_code}, {resp_stream.reason})")

                file_size = int(resp_stream.headers.get("Content-Length", -1))
                if file_size == -1:
                    raise Exception("Could not determine file size")
            
                with ProgressBar(file_size, width=30) as bar:
                    with open(dest, "wb") as f:
                        n_read = 0
                        for data in resp_stream.iter_content(chunk_size):
                            if do_quit:
                                print(red(" (Cancelled)"), end="")
                                f.close()
                                os.remove(dest)
                                raise QuitProgram()

                            n_read += f.write(data)
                            bar.update(n_read)

        except requests.ConnectTimeout:
            raise Exception("Timeout. Is your VPN connected?")
    
    return dest

def zip_dir(src_dir: str, dst: str):
    if not isinstance(src_dir, str):
        raise TypeError("src_dir must be a str")
    
    if not isinstance(dst, str):
        raise TypeError("dst must be a str")
    
    # Ensure directory exists
    src_dir = os.path.abspath(src_dir)
    if not os.path.isdir(src_dir):
        raise NotADirectoryError(src_dir)
    
    # Zip all entries
    dst = os.path.abspath(dst)
    if ask_user_replace_file(dst):
        parent_dir = os.path.dirname(dst)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        print(f"Zipping directory...")
        with zipfile.ZipFile(dst, "w") as zip:
            for entry in os.listdir(src_dir):
                path = os.path.join(src_dir, entry)
                print("  Adding", os.path.relpath(path))
                zip.write(path, arcname=entry)

        return True

    return False


def send_mod_hashes(url: str):
    data = _init_mod_hash_table()
    try:
        resp = requests.post(url, json=data)
    except Exception as e:
        raise e

    if resp.status_code != 200:
        raise Exception("Failed to post data")



### PROGRAM ROUTINES ###

def _init_directories():
    """Set CWD and create required directories"""

    # Move to directory which contains this file
    os.chdir(os.path.dirname(__file__))

    # Create cache directories
    if not os.path.exists(PATH_CACHE):
        os.makedirs(PATH_CACHE)

    if not os.path.exists(PATH_DOWNLOADS):
        os.makedirs(PATH_DOWNLOADS)

def _init_mod_hash_table():
    """Create mods hash file if it doesn't already exist"""

    table = dict()

    if not os.path.exists(PATH_MOD_HASHES):
        mods_dir = os.path.join(get_minecraft_dir(), "mods")

        print("Initializing mods hash table... ", end="", flush=True)

        for mod in (f for f in os.listdir(mods_dir) if os.path.isfile(os.path.join(mods_dir, f))):
            with open(os.path.join(mods_dir, mod), "rb") as file:
                table.update({mod: hashlib.sha256(file.read()).hexdigest()})
        
        with open(PATH_MOD_HASHES, "w") as file:
            file.write(json.dumps(table))

        print("Done")
    else:
        with open(PATH_MOD_HASHES, "r") as file:
            table = json.loads(file.read())

    return table

def setup():
    # Quit gracefully on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    _init_directories()
    _init_mod_hash_table()


def zip_mods(src_dir: str, dst: str):
    # Ensure directory exists
    src_dir = os.path.abspath(src_dir)
    if not os.path.isdir(src_dir):
        raise Exception(f"Directory does not exist: {os.path.relpath(src_dir)}")
    
    # Validate directory form (can only contain .jar files)
    entries = os.listdir(src_dir)
    dirs = tuple(d for d in entries if os.path.isdir(os.path.join(src_dir, d)))
    files = tuple(f for f in entries if os.path.isfile(os.path.join(src_dir, f)))

    if dirs:
        raise Exception("The provided directory should not contain directories")

    if not files:
        raise Exception("The provided directory is empty")

    for file in files:
        if not file.endswith(".jar"):
            raise Exception("All files in the provided directory should be a .jar")
    
    # Zip it
    dst = os.path.abspath(dst)
    if zip_dir(src_dir, dst):
        print("Successfully created", os.path.relpath(dst))

def update_client_mods():
    # Download new mods
    new_mods_zip = download_file(FILE_SERVER_ADDR + MOD_PACK_ENDPOINT, "mods.zip")
    with zipfile.ZipFile(new_mods_zip) as zip:
        new_mods_filenames = set(entry.filename for entry in zip.infolist())

    # Tally existing mods
    mods_dir = os.path.join(get_minecraft_dir(), "mods")
    existing_mods_filenames = set(f for f in os.listdir(mods_dir) if os.path.isfile(os.path.join(mods_dir, f)))

    # Display which mods will be added (A), updated (U), and deleted (D).
    # Then ask the user if they want to continue.
    # for m in sorted(new_mods_filenames - existing_mods_filenames):
    #     print(" ", green("A:"), m)
    # for m in sorted(existing_mods_filenames & new_mods_filenames):
    #     print(" ", yellow("U:"), m)
    for m in sorted(existing_mods_filenames - new_mods_filenames):
        print(" ", red("D:"), m)

    if ask_user_yes_no("Continue?"):
        # Remove existing mods
        for filename in existing_mods_filenames:
            os.remove(os.path.join(mods_dir, filename))
        
        # Extract new mods
        print(f"Updating mods ({len(new_mods_filenames)})...")
        with zipfile.ZipFile(new_mods_zip) as zip:
            for item in zip.infolist():
                print("  Installing", item.filename)
                zip.extract(item, mods_dir)
        print("Successfully updated mods")

        # Delete downloaded zip
        # os.remove(new_mods_zip_abspath)

def update_client_shaders():
    # Download shaderpack
    shaderpack = download_file(FILE_SERVER_ADDR + SHADER_PACK_ENDPOINT, SHADER_PACK_ENDPOINT)

    # Install/replace the shaderpack
    shaderpacks_dir = os.path.join(get_minecraft_dir(), "shaderpacks")
    dest = os.path.join(shaderpacks_dir, SHADER_PACK_ENDPOINT)
    if ask_user_replace_file(dest):
        shutil.copyfile(shaderpack, dest)
        print("Successfully installed shaderpack")
    
def clear_cache():
    shutil.rmtree(PATH_CACHE)



### MAIN PROGRAM ###

def main():
    # Init command line parser
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
                        nargs=2,
                        metavar=("DIR", "FILE"),
                        help="Compress all mods in DIR to a zip file FILE.")
    parser.add_argument("--clear-cache",
                        action="store_true",
                        help="Clear your local cache.")

    try:
        # Parse args and setup
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
        print(red(e))
        parser.print_usage()
    except QuitProgram as e:
        print("Quitting...")
        # raise e
    except Exception as e:
        print(red(e))
        # raise e

if __name__ == "__main__":
    main()
