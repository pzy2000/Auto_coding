import os
import time
from tqdm import tqdm

d = "repos"
for dirpath, dirnames, filenames in tqdm(os.walk(d)):
    '''print(dirpath)
    print(dirnames)
    print(filenames)'''
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        if full_path.endswith(".py"):
            # print(f"keeping {full_path}")
            pass
        else:
            # print(f"deleting {full_path}")
            if d in full_path:
                try:
                    os.remove(full_path)
                except PermissionError:
                    pass
            else:
                print("something went wrong!")
                time.sleep(60)
    # break
