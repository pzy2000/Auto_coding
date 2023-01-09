from time import sleep
from github import Github
import time
from datetime import datetime
import os
from http.client import RemoteDisconnected
# 1.增加下面两行
import urllib3
from urllib3.exceptions import ProtocolError
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

urllib3.disable_warnings()
with open("token.txt", "r") as f:
    access_token = f.read()
g = Github(access_token)
print(g.get_user())
end_time = time.time() - 86400000
start_time = end_time - 8640000

for i in range(5):
    start_time_str = datetime.utcfromtimestamp(start_time).strftime("%Y-%m-%d")
    end_time_str = datetime.utcfromtimestamp(end_time).strftime("%Y-%m-%d")
    query = f"language:c++ created:{start_time_str}..{end_time_str}"
    print(query)

    result = g.search_repositories(query)
    print(result.totalCount)
    for repository in result:
        print(f"{repository.clone_url}")
        try:
            os.system(f"git clone {repository.clone_url} "
                      f"G:/repos_qt/{repository.owner.login}/{repository.name}")
        except ConnectionError:
            print('ConnectionError')
        except ProtocolError:
            print('ProtocolError')
        except RemoteDisconnected:
            print('RemoteDisconnected')
        except Exception:
            print('Unexpected error')
        sleep(1)
