import multiprocessing
from multiprocessing import Pool
import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path
from pathlib import PurePath


def getfiles():
    root = tk.Tk()
    root.withdraw()
    file_paths = fd.askopenfilenames()
    files = []
    count = 0
    for fp in file_paths:
        filepath = Path(fp)
        print(filepath)
        count += 1
        files.append((filepath, f"{count}"))
    print(f"{count} files selected.")
    return files

def renameFile(file):
    dir_ = file[0].parent
    suffix_ = file[0].suffix
    name_ = file[2] + file[1] + suffix_
    old = file[0]
    new_path = Path(dir_, name_)
    if Path.exists(new_path):
        print(f"File {new_path.stem} exists. Skipping.")
    old.rename(new_path)
    
def removeSym(file):
    dir_ = file[0].parent
    suffix_ = file[0].suffix
    name_ = "".join(f for f in file[0].stem if f.isalpha()) + suffix_
    old = file[0]
    new_path = Path(dir_, name_)
    if Path.exists(new_path):
        print(f"File {new_path.stem} exists. Skipping.")
        return
    old.rename(new_path)
    
def toCap(file):
    dir_ = file[0].parent
    suffix_ = file[0].suffix
    name_ = file[0].stem.upper() + suffix_
    old = file[0]
    new_path = Path(dir_, name_)
    old.rename(new_path)
    
def toLow(file):
    dir_ = file[0].parent
    suffix_ = file[0].suffix
    name_ = file[0].stem.lower() + suffix_
    old = file[0]
    new_path = Path(dir_, name_)
    old.rename(new_path)
    
def attachDir(file):
    folder = PurePath(file[0]).parts
    dir_ = file[0].parent
    suffix_ = file[0].suffix
    name_ =  folder[-2] + "_" + file[0].stem + suffix_
    old = file[0]
    new_path = Path(dir_, name_)
    if Path.exists(new_path):
        print(f"File {new_path.stem} exists. Skipping.")
    old.rename(new_path)
    
def pool_handler(mode):
    p = Pool(multiprocessing.cpu_count() - 1)
    if mode in "rename":
        p.map(renameFile, replace)
        print("Rename complete.")
    elif mode in "rem num sym":
        p.map(removeSym, files)
        print("Numbers and symbols removed.")
    elif mode in "capitalize":
        p.map(toCap, files)
        print("Capitalization complete.")
    elif mode in "lowercase":
        p.map(toLow, files)
        print("Lowercase complete.")
    elif mode in "attach folder name":
        p.map(attachDir, files)
        print("Folder name attached.")
    else:
        print("Invalid command.")


if __name__ == '__main__':
    files = getfiles()
    choice = input("func: ")
    if choice in "rename":
        new_name = input("new name: ")
        replace = [(f[0], f[1], new_name) for f in files]
    pool_handler(choice)