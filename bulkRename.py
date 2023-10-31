from multiprocessing import Pool
import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path


def getfiles():
    root = tk.Tk()
    root.withdraw()
    file_paths = fd.askopenfilenames()
    files = []
    i = 1
    for fp in file_paths:
        filepath = Path(fp)
        print(filepath)
        files.append((filepath, f"{i}"))
        i+=1
    return files

def renameFile(file):
    dir_ = file[0].parent
    suffix_ = file[0].suffix
    name_ = file[2] + file[1] + suffix_
    old = file[0]
    new_path = Path(dir_, name_)
    old.rename(new_path)
    print(new_path)
    
def pool_handler():
    p = Pool(4)
    p.map(renameFile, replace)


if __name__ == '__main__':
    files = getfiles()
    new_name = input("Rename: ")
    replace = [(f[0], f[1], new_name) for f in files]
    pool_handler()