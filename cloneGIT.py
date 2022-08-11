from time import sleep
from github import Github
import time
from datetime import datetime
import os
# 1.增加下面两行
import urllib3

urllib3.disable_warnings()
with open("token.txt", "r") as f:
    access_token = f.read()
g = Github(access_token)
print(g.get_user())
end_time = time.time() - 2000000
start_time = end_time - 86400

for i in range(5):
    start_time_str = datetime.utcfromtimestamp(start_time).strftime("%Y-%m-%d")
    end_time_str = datetime.utcfromtimestamp(end_time).strftime("%Y-%m-%d")
    query = f"django language:python created:{start_time_str}..{end_time_str}"
    print(query)
    end_time -= 86400
    start_time -= 86400
    result = g.search_repositories(query)

    print(result.totalCount)

    for repository in result:
        print(f"{repository.clone_url}")
        os.system(f"git clone {repository.clone_url} "
                  f"repos/{repository.owner.login}/{repository.name}")
        sleep(1)
