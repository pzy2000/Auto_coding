import os
import time
from tqdm import tqdm

d = "G:/repos_qt"
for dirpath, dirnames, filenames in tqdm(os.walk(d)):
    # print(dirpath)
    # print(dirnames)

    for f in filenames:
        full_path = os.path.join(dirpath, f)
        if full_path.endswith(".cpp") or full_path.endswith(".hpp") or \
                full_path.endswith(".cxx") or full_path.endswith(".cc") or \
                full_path.endswith(".h") or full_path.endswith(".C") or \
                full_path.endswith(".hxx"):
            print(f)
        else:
            if d in full_path:
                try:
                    os.remove(full_path)
                except PermissionError:
                    pass
            else:
                print("something went wrong!")
                time.sleep(60)
