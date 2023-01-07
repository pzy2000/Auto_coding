import os
import time
from tqdm import tqdm

d = "/root/repos_qt"
for dirpath, dirnames, filenames in tqdm(os.walk(d)):
    print(dirpath)
    print(dirnames)
    print(filenames)
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        if full_path.endswith(".cpp"):
            pass
        else:
            if d in full_path:
                try:
                    os.remove(full_path)
                except PermissionError:
                    pass
            else:
                print("something went wrong!")
                time.sleep(60)
