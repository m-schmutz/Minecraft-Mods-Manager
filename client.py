try:
    import os
    import sys
    import signal
    import typing
    import zipfile
    import requests
except ModuleNotFoundError as e:
    print("Python module not installed:", e)
    quit()



### CONSTANTS ###

FILE_SERVER_ADDR = "http://172.30.1.1:8000/files/"

OUTPUT_DIR_ABSPATH: str
CURRENT_DIR_ABSPATH: str
DOWNLOADS_DIR_ABSPATH: str
NUM_PROGRAM_OPTIONS: int
VALID_PROGRAM_OPTIONS_RESPONSES: tuple[str]
PROGRAM_OPTIONS_STRING: str



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

CallbackType = typing.Callable[[None],None]

class ProgramOption:
    def __init__(self,
                 name: str,
                 callback: CallbackType,
                 switches: tuple[str] = None,
                 *,
                 is_developer: bool = False):
        self.name = name
        self.callback = callback
        self.switches = switches
        self.is_developer = is_developer # currently only used in interactive mode to display as gray

    def _raise_if_bad(self):
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        
        if not callable(self.callback):
            raise TypeError("callback must be callable")
        
        if self.switches is not None:
            for switch in self.switches:
                if not isinstance(switch, str):
                    raise TypeError("All switches must be a string")
        
        if not isinstance(self.is_developer, bool):
            raise TypeError("is_developer must be a boolean")


def setup():
    global CURRENT_DIR_ABSPATH
    global DOWNLOADS_DIR_ABSPATH
    global OUTPUT_DIR_ABSPATH
    global PROGRAM_OPTIONS
    global NUM_PROGRAM_OPTIONS
    global VALID_PROGRAM_OPTIONS_RESPONSES
    global PROGRAM_OPTIONS_STRING


    # Catch Ctrl+C
    signal.signal(signal.SIGINT, raise_quit_exception)


    # Validate all program options are set correctly
    for po in PROGRAM_OPTIONS:
        po._raise_if_bad()


    # Move to directory which contains this file
    CURRENT_DIR_ABSPATH = os.path.abspath(os.path.dirname(__file__))
    if os.path.isdir(CURRENT_DIR_ABSPATH):
        os.chdir(CURRENT_DIR_ABSPATH)
    else:
        raise Exception("Cannot determine current path")


    # Create downloads directory
    DOWNLOADS_DIR_ABSPATH = os.path.abspath("downloads")
    if not os.path.exists(DOWNLOADS_DIR_ABSPATH):
        os.makedirs(DOWNLOADS_DIR_ABSPATH)
    
    # Create output directory
    OUTPUT_DIR_ABSPATH = os.path.abspath("output")
    if not os.path.exists(OUTPUT_DIR_ABSPATH):
        os.makedirs(OUTPUT_DIR_ABSPATH)


    # Set program options helper info. Make developer options gray and italic.
    NUM_PROGRAM_OPTIONS = len(PROGRAM_OPTIONS)
    VALID_PROGRAM_OPTIONS_RESPONSES = tuple(str(i) for i in range(1, NUM_PROGRAM_OPTIONS + 1))
    program_option_lines = list()
    for i,po in enumerate(PROGRAM_OPTIONS):
        line = str()
        if po.is_developer:
            line += "\x1b[3;90m"
        line += f"({VALID_PROGRAM_OPTIONS_RESPONSES[i]}) {po.name}"
        if po.is_developer:
            line += "\x1b[0m"
        program_option_lines.append(line)
    PROGRAM_OPTIONS_STRING = "\n".join(program_option_lines)

def parse_cmdline():
    global PROGRAM_OPTIONS

    tasks: list[CallbackType] = []
    for arg in sys.argv:
        for po in PROGRAM_OPTIONS:
            if po.switches is not None and arg in po.switches:
                tasks.append(po.callback)
    
    return tasks


def zip_client_mods():
    global CURRENT_DIR_ABSPATH
    global OUTPUT_DIR_ABSPATH
    
    # The directory containing all client-side mods
    input_dir_abspath = os.path.join(CURRENT_DIR_ABSPATH, "resources/mods")
    if not os.path.isdir(input_dir_abspath):
        raise Exception("Cannot find mods to zip")
    
    # The zipfile to create
    output_file_abspath = os.path.join(OUTPUT_DIR_ABSPATH, "mods.zip")
    if ask_user_replace_file(output_file_abspath):
        file = zip_dir(input_dir_abspath, OUTPUT_DIR_ABSPATH)
        print("Successfully created", os.path.relpath(file))

def update_client_mods():
    # Determine path to local .minecraft directory
    dot_minecraft_dir_abspath = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft")
    if not os.path.exists(dot_minecraft_dir_abspath):
        raise Exception("Could not locate .minecraft directory")

    # Download new mods
    new_mods_zip_abspath = download_file(FILE_SERVER_ADDR + "ModPack.zip", "mods.zip")
    with zipfile.ZipFile(new_mods_zip_abspath) as zip:
        new_mod_filenames = set(entry.filename for entry in zip.infolist())

    # Gather existing mod names
    mods_dir_abspath = os.path.join(dot_minecraft_dir_abspath, "mods")
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



### MAIN PROGRAM ###

PROGRAM_OPTIONS = (
    ProgramOption("Quit", raise_quit_exception),
    ProgramOption("Update Mods", update_client_mods, ("-u", "--update")),
    ProgramOption("Zip Mods", zip_client_mods, ("-z", "--zip"), is_developer=True),
)

def main():
    global PROGRAM_OPTIONS
    global VALID_PROGRAM_OPTIONS_RESPONSES
    global PROGRAM_OPTIONS_STRING
    
    try:
        setup()
        tasks = parse_cmdline()

        if tasks:
            # Run specified tasks then quit
            for task in tasks:
                task()
        else:
            # Run interactively
            while True:
                print(PROGRAM_OPTIONS_STRING)
                user_resp = ask_user(" > ", VALID_PROGRAM_OPTIONS_RESPONSES, show_responses=False)
                index = int(user_resp) - 1
                PROGRAM_OPTIONS[index].callback()
    except QuitException:
        print("Quitting...")
    except Exception as e:
        print(f"Terminating from exception: \x1b[91m{e}\x1b[0m") # red message
        raise e

if __name__ == "__main__":
    main()
