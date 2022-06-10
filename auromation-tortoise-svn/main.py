import sys, subprocess, os, re

class list(list):
    def __init__(self, *args):
        super().__init__(args)
    def get(self, text_):
        if not text_ in self:
            return False
        return True
    def getValue(self, elm, default = False, one_up=True):
        if not elm in self:
            return default
        index = self.index(elm)
        try:
            return self[index] if not one_up else self[index + 1]
        except IndexError:
            print("No value is provided to the argument %s" % elm)
            sys.exit()
def main(arguments: list):
    help_text = """
    syntax:
        python filename.py url [options] [.help]
    options:
        url:
            URL to the repo/folder of github
        options:
            -e filename/filepath
                Download and execute file in given path
            -f
                Download specific folder
                    Note: url must be in a pattern of
                        https://github.com/[username]/[repo_name]/tree/[branch]/[folder_name]
                            If specific file is to be downloaded, url pattern must be like
                                https://github.com/[username]/[repo_name]/tree/[branch]/[folder_name]/[filename.ext]
            -p path
                Specify path to download folder to.
                    (Default: current)
        .help:
            Display this help messages and exit
    """

    filename = os.path.basename(__file__)
    if filename in arguments[0]:
        arguments.pop(0) # removing filename -- main.py
    if len(arguments) <= 0:
        print(help_text)
        sys.exit()
    arguments = list(*arguments)
    if arguments.get(".help"):
        print(help_text)
        sys.exit()
    git_url = arguments[0]
    if git_url == '' or git_url == None:
        print("URL is required")
        sys.exit()
    file_path = arguments.getValue("-e")
    getFolder = arguments.get("-f")
    getPath = arguments.getValue("-p", ".")
    if getFolder:
        # https://github.com/sachin-acharya-projects/automation-with-python
        listing = str(git_url).split('/')
        try:
            cur = listing.index('tree')
            branch_name = listing[index + 1]
            git_url = git_url.replace('%s/%s' % ('tree', branch_name), 'trunk')
        except ValueError:
            pass
    print("Downloading from GitHub")
    print("This will overide existing files or folder\n[Continue?]")
    if input("").lower() == 'exit':
        sys.exit()
    try:
        output = subprocess.check_output("svn export %s %s --force" % (git_url, getPath), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        #  svn export https://github.com/sachin-acharya-projects/automation-with-python/trunk --force
        print("It seems you have not download Tortoise SVN\nDownload Here: https://tortoisesvn.net/downloads.html")
    if file_path:
        print("Executing file %s" % file_path)
        if '.py' in file_path:
            os.system("python %s" % file_path)
        else:
            os.system("start %s" % file_path) # Currenly only for windows
if __name__ == '__main__':
    main(sys.argv)