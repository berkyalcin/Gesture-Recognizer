from os import system


class Setup:
    def __init__(self, dependencies_file="dependencies.txt"):
        f = open(dependencies_file, "r")
        f = f.readlines()
        for depend in f:
            splitted = depend.split()
            try:
                system(f"pip install {splitted[0]}")
            except:
                system(f"pip3 install {splitted[0]}")
