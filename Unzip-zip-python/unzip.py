# Zip/Unzip Archive in Python

from tkinter import Tk, filedialog
from zipfile import ZipFile
import os, colorama, stat, sys
from py_setenv import setenv

argv = sys.argv[1:]

colorama.init(autoreset=True)

root = Tk()
PATH = os.path.dirname(os.path.abspath(__file__))
root.withdraw()
root.attributes('-topmost', True)
root.title("Zip/Unzip Archive in Python")
root.iconbitmap(os.path.join(PATH, 'icon.ico'))

# help text

help_text = f"""Use this command-line tool to manage your archive files.

usage: unzip.py [options] [file]

(Note: boolean options are valueless)

options
    -h, --help                           Show this help message and exit.
    create (bool)                        Create a new archive.
    
        paths (string)                   Paths to archive files.
        --ignore (bool)                  Paths and files to ignore. (Will be asked from the user during run-time)
        --ignore-path (bool)             Paths to ignore. (Will be asked from the user during run-time)
        folder (string)                  Basefolder for members of new archive.
        --show-skipped (bool)            Display skipped files and folder in the console.
        --ignore-from-file (bool)        Read content from file ".ignore" and ignore those files.
        --choose-path (bool)             Choose path to create archive.
        --choose-files (bool)            Choose files to create archive.
        
    extract (bool)                       Extract an archive.
            destination (string)         Destination folder to extract. 
            --choose-destination (bool)  Choose destination folder graphically.
            --filelist (bool)            Files that are to be extracted from archive. (Will be asked from the user during run-time)
            --search-all (bool)          Search for the similar pattern of file name (eg. filename.ext is equal to dirname/filename.exe if passed).
            --fast (bool)                Extract all the files quickly.
    
    read (bool)                          Read The archive passed.

file (string)                            Path to archive file.

--add-path (bool)                        Add CURRENT_DIRECTORY to SYSTEM PATH
"""

# Function to choose files to zip
def choose_files(default, title="Choose files to Archive"):
    files = filedialog.askopenfilenames(title=title, filetypes=[("All Files", "*.*")])
    return list(files) if not files == '' else default

# Function to choose destination folder
def choose_destination(default, title="Choose destination folder"):
    destination = filedialog.askdirectory(title=title)
    return destination if not destination == '' else default

# Convert argv into dictionary
def argumentParser():
    argumentList = {}
    def_list = [
        "paths",
        "folder",
        "destination",
        "create",
        "extract",
        "read"
    ]
    if "--help" in argv or "-h" in argv or len(argv) == 0:
        print()
        sys.exit(f"{colorama.Fore.LIGHTCYAN_EX}{help_text}")
    if '--add-path' in argv:
        if not PATH in setenv("path", suppress_echo=True, user=True).split(";"):
            setenv("path", value=PATH, append=True, user=True, suppress_echo=True)
    for count, elem in enumerate(argv):
        if elem.startswith("-") and not elem.startswith("--"):
            try:
                tem_elem = elem.replace("-", "", 1).replace("-", "_")
                if argumentList.get(tem_elem, None) is None:
                    argumentList[tem_elem] = argv[count + 1]
            except IndexError:
                pass
        elif elem.startswith('--'):
            tem_elem = elem.replace("--", "", 1).replace("-", "_")
            if argumentList.get(tem_elem, None) is None:
                argumentList[tem_elem] = True
        else:
            if elem in def_list:
                if elem == "create" or elem == "extract" or elem == "read":
                    argumentList[elem] = True
                else:
                    argumentList[elem] = elem
            else:
                argumentList["file"] = elem
    checking_port = [
        "ignore",
        "ignore_path",
        "filelist"
    ]
    
    for checking in checking_port:
        if argumentList.get(checking, False):
            print("Enter the values for {} (Separate values with ; incase of multiple values)".format(checking))
            while True:
                val = input("> ")
                if not val == '':
                    break
                print(f"{colorama.Fore.RED}Invalid input. Please try again.")
            argumentList[checking] = [x.removeprefix(" ") for x in val.split(";")]
            
    county = [
        "choose_path",
        "choose_files",
        "choose-destination"
    ]
    
    for checking in county:
        if argumentList.get(checking, False):
            argumentList[f"{checking}_"] = True
            argumentList.pop(checking)
    return argumentList
class ZipArchive:
    def __init__(self, archive: str = 'unzip-zipper.zip'):
        self.archive = archive
        print("{}ZipArchive started\n".format(colorama.Fore.LIGHTCYAN_EX))
    def create(
            self, 
            paths = None,
            ignore: list = None, 
            ignore_path: list = None, 
            folder: str = None, 
            show_skipped: bool = False, 
            ignore_from_file: bool = False,
            choose_path_: bool = False,
            choose_files_: bool = False,
            **_
        ):
        if choose_path_:
            paths = [choose_destination(paths, "Choose Path to Archive")]
        if choose_files_:
            choosen_files = choose_files(None, "Choose Files to Archive")
            if not choosen_files is None:
                if paths is None:
                    paths = choosen_files
                else:
                    paths = paths + choosen_files
        if paths is None:
            paths = ['.']
        filename = []
        fileExtentsion = []
        filelist = []
        if ignore_from_file:
            if os.path.exists('.ignore'):
                with open('.ignore', 'r') as f:
                    if ignore is None:
                        ignore = f.read().splitlines()
                    else:
                        ignore = ignore + f.read().splitlines()
        if not ignore is None:
            for ingnoring in ignore:
                if "*" in ingnoring:
                    tempT = os.path.splitext(ingnoring)
                    if not str(tempT[0]) == '*':
                        filename.append(str(tempT[0]))
                    if not str(tempT[1]) == '*':
                        fileExtentsion.append(str(tempT[1]))
                else:
                    filename.append(str(ingnoring))
        folder_skipped_count = 0
        for path in paths:
            print("{}Searching in path {}\n".format(colorama.Fore.LIGHTCYAN_EX, path))
            if os.path.exists(os.path.abspath(path)) and os.path.isdir(os.path.abspath(path)):
                for root, _, files in os.walk(path):
                    if ignore_path is not None and any(os.path.abspath(root).startswith(os.path.abspath(i)) for i in ignore_path):
                        if show_skipped:
                            print(f"{colorama.Fore.LIGHTMAGENTA_EX}Skipped {os.path.abspath(root)}")
                            folder_skipped_count += 1
                        continue
                    else:
                        print("{}Scanning {}\n".format(colorama.Fore.LIGHTCYAN_EX, os.path.abspath(root)))
                    for file in files:
                        if file == self.archive:
                            continue
                        tempE = os.path.splitext(file)
                        if str(tempE[0]) in filename or str(tempE[1]) in fileExtentsion or str(file) in filename:
                            continue
                        filelist.append([os.path.join(root, file), path])
            else:
                if os.path.exists(path):
                    filelist.append([path, '*'])
        print(f"{colorama.Fore.LIGHTCYAN_EX}Scanning Complete\n")
        with ZipFile(self.archive, 'a') as zipfile:
            namelist = zipfile.namelist()
            skipped_count = 0
            for file, pth in filelist:
                if pth == '*':
                    basepath = os.path.basename(file)
                else:
                    basepath = str(file).removeprefix(pth)
                if folder is not None:
                    basepath = folder + basepath
                if basepath.removeprefix("\\").replace('\\', '/') in namelist:
                    if show_skipped:
                        print(f"{colorama.Fore.LIGHTMAGENTA_EX}Skipped {basepath}")
                    skipped_count += 1
                    continue
                tem = basepath.removeprefix('\\')
                print(f"{colorama.Fore.LIGHTCYAN_EX}Adding {tem}")
                try:
                    zipfile.write(file, basepath)
                except Exception as e:
                    print(f"{colorama.Fore.LIGHTRED_EX}Error: {e}")
        if not skipped_count == 0:
            print(f"{colorama.Fore.LIGHTBLUE_EX}\nNote: Dublicate files were skipped. ")
            print("{}Total {} files and {} folders were skipped.\n".format(colorama.Fore.LIGHTBLUE_EX, skipped_count, folder_skipped_count))
        print("{}\nFollowing Paths have been added to the Archive {}\n".format(colorama.Fore.LIGHTCYAN_EX, self.archive))
        longdash = "_" * 60
        print(f"{colorama.Fore.LIGHTCYAN_EX}{longdash}\n")
        for path in paths:
            print(f"{colorama.Fore.LIGHTCYAN_EX}\"%s\"" % os.path.abspath(path))
    def read(self):
        if not os.path.exists(self.archive):
            print("{}Archive {} doesnot exist\n".format(colorama.Fore.LIGHTRED_EX, self.archive))
            return
        with ZipFile(self.archive, 'r') as zipfile:
            print(f"{colorama.Fore.LIGHTCYAN_EX}Reading Archive {self.archive}\n")
            print("{}{:<46} {:<22} {:<10} {:<10}".format(colorama.Fore.CYAN, 'Filename','Modified','Size','File Mode'))
            print("{}{}".format(colorama.Fore.CYAN, '_' * 92))
            print("\n")
            total_size = 0
            for zinfo in zipfile.filelist:
                date = "%d-%02d-%02d %02d:%02d:%02d" % zinfo.date_time[:6]
                print("{}{:<46} {:<22} {:<10} {:<10}".format(colorama.Fore.CYAN, zinfo.filename, date, zinfo.file_size, stat.filemode(zinfo.external_attr >> 16)))
                total_size += zinfo.file_size
            print("\n")
            print("{}Total Size: {}".format(colorama.Fore.CYAN, total_size))
    def extract(self, 
            destination: str = '.', 
            choose_destination_: bool = False, 
            filelist: list = None, 
            search_all: bool = False, 
            fast=True,
            **_
        ):
        if choose_destination_:
            destination = choose_destination()
        if not os.path.exists(destination):
            os.mkdir(destination)
        with ZipFile(self.archive, 'r') as zipfile:
            # check if the items in the filelist are in the archive
            if not filelist is None:
                file_namelist = zipfile.namelist()
                for file in list(filelist):
                    if not file in file_namelist:
                        lenght = 0
                        if search_all:
                            temp_filelist = [n for n in file_namelist if file in n]
                            filelist = filelist + temp_filelist
                            lenght = len(temp_filelist)
                        if lenght == 0:
                            print(f"{colorama.Fore.LIGHTRED_EX}Skipping: File {file} is not in the archive")
                        filelist.remove(file)
            if fast:
                zipfile.extractall(destination, filelist)
                t_i = "\n ".join(filelist)
                print(f"{colorama.Fore.LIGHTCYAN_EX}Following Files were extracted\n {t_i}")
            else:
                for file in filelist:
                    print(f"{colorama.Fore.LIGHTCYAN_EX}Extracting {destination}/{file}")
                    zipfile.extract(file, destination)

if __name__ == '__main__':
    argumentList = argumentParser()
    archiveFile = argumentList.get('file', 'unzip-zipper.zip')
    create_zip = ZipArchive(archiveFile)
    if argumentList.get('create', False):
        create_zip.create(**argumentList)
    if argumentList.get('read', False):
        create_zip.read()
    if argumentList.get('extract', False):
        create_zip.extract(**argumentList)