import os
import time
from tqdm import tqdm

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256
d = "repos"
NEWLINECHAR = "<N>"

full_paths = []
for dirpath, dirnames, filenames in tqdm(os.walk(d)):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        full_paths.append(full_path)

print(len(full_paths))

with open("code_text_data.txt", "a") as f:
    for fpath in full_paths:
        try:
            data = open(fpath, 'r', encoding='utf-8').read()
            fd = data.replace("\n", NEWLINECHAR)
            if 100 < len(data) <= MAX_CHAR_LENGTH:
                f.write(fd + '\n')
            else:
                sd = data.split(f"{NEWLINECHAR}{NEWLINECHAR}")
                substring = ""
                for split in sd:
                    substring += split + f"{NEWLINECHAR}{NEWLINECHAR}"
                    if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                        f.write(substring + "\n")
                        substring = ""
        except Exception as e:
            print(str(e))
