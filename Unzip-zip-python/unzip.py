# Zip/Unzip Archive in Python

from zipfile import ZipFile
import os, colorama, stat
from tkinter import Tk, filedialog

colorama.init(autoreset=True)

root = Tk()

root.withdraw()
root.attributes('-topmost', True)
root.title("Zip/Unzip Archive in Python")
root.iconbitmap('icon.ico')

# Function to choose files to zip
def choose_files(default, title="Choose files to Archive"):
    files = filedialog.askopenfilenames(title=title, filetypes=[("All Files", "*.*")])
    return list(files) if not files == '' else default

# Function to choose destination folder
def choose_destination(default, title="Choose destination folder"):
    destination = filedialog.askdirectory(title=title)
    return destination if not destination == '' else default

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
            choose_files_: bool = False
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
        for path in paths:
            print("{}Searching in path {}\n".format(colorama.Fore.LIGHTCYAN_EX, path))
            if os.path.exists(os.path.abspath(path)) and os.path.isdir(os.path.abspath(path)):
                for root, _, files in os.walk(path):
                    print("{}Scanning {}\n".format(colorama.Fore.LIGHTCYAN_EX, os.path.abspath(root)))
                    if ignore_path is not None and any(root in ignore_path, os.path.abspath(root) in ignore_path):
                        continue
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
            print("{}Total {} files were skipped.\n".format(colorama.Fore.LIGHTBLUE_EX, skipped_count))
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
            for zinfo in zipfile.filelist:
                date = "%d-%02d-%02d %02d:%02d:%02d" % zinfo.date_time[:6]
                print("{}{:<46} {:<22} {:<10} {:<10}".format(colorama.Fore.CYAN, zinfo.filename, date, zinfo.file_size, stat.filemode(zinfo.external_attr >> 16)))
    def extract(self, 
            destination: str = '.', 
            choose_destination_: bool = False, 
            filelist: list = None, 
            search_all: bool = False, 
            fast=True
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

# TODO: Add CLI arguments
if __name__ == '__main__':
    # Testing Functionality
    create_zip = ZipArchive(archive='right.zip')
    # create_zip.create(ignore_from_file=True, show_skipped=True, choose_files_=False, choose_path_= False, paths=['test_folder'])
    # create_zip.extract(destination='NewFolder', filelist=['file.py', 'file.txt'], search_all=True, choose_destination_=False, fast=False)
    create_zip.read()