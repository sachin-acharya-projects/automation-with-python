import sys, subprocess

def main(arguments: list):
    arguments.remove(sys.path.basename(__name__)) # removing filename
    pass
if __name__ == '__main__':
    main(sys.argv)