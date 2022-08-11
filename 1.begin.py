from time import sleep
from github import Github

access_token = open("token.txt", "r").read()
g = Github(access_token)
print(g.get_user())
query = "pygame language:python created:2022-08-08..2022-08-09"
print(query)

result = g.search_repositories(query)


print(result.totalCount)

for repository in result:
    print(f"{repository.clone_url}")
    sleep(1)
