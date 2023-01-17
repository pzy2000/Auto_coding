import os
from tqdm import tqdm

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256
d = "G:/repos_qt"
NEWLINECHAR = "<N>"
print("开始读取文件目录:")
full_paths = []
for dirpath, dirnames, filenames in tqdm(os.walk(d)):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        full_paths.append(full_path)

print(len(full_paths))
print("开始写入数据集:")

with open("code_text_data.txt", "a") as f:
    for fpath in tqdm(full_paths):
        try:
            with open(fpath, 'r') as fuck:
                data = fuck.read()
            fd = data.replace("\n", NEWLINECHAR)
            if 100 < len(data) <= MAX_CHAR_LENGTH:
                if "Copyright" in fd:
                    print("FUCKER: ", fd)
                    continue
                f.write(fd + '\n')
                print(fd + '\n')
            else:
                sd = data.split(f"{NEWLINECHAR}{NEWLINECHAR}")
                substring = ""
                for split in sd:
                    substring += split + f"{NEWLINECHAR}{NEWLINECHAR}"
                    if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                        if "Copyright" in substring:
                            print("FUCKER: ", substring)
                            continue
                        f.write(substring + "\n")
                        print(substring + "\n")
                        substring = ""
                    # 处理>512的情况!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        except Exception as e:
            pass
            # print(str(e))
