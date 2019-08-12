import requests


def get_github_token():
    path = "metadata/github-token.txt"
    file = open(path, "r")
    token = file.readline().strip()
    user = file.readline().strip()
    return user, token


user_id, api_token = get_github_token()  # read my pull requests

url = "https://api.github.com/graphql"

# , states: MERGED OPEN CLOSED
# https://developer.github.com/v4/explorer/
query = """
{
  user(login: "%s") {
    pullRequests(first: 100) {
      totalCount
      nodes {
        createdAt
        number
        title
        closedAt
        closed
        deletions
        merged
        mergedAt
        mergedBy {
          login
        }
        permalink
        repository {
          id
        }
        state
        url
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

query = query % user_id

json = {"query": query}

# https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line
headers = {"Authorization": "token %s" % api_token}

response = requests.post(url=url, json=json, headers=headers)
data = response.json()
prs = data["data"]["user"]["pullRequests"]["nodes"]

merged = list()
active = list()
for pr in prs:
    if pr["merged"]:
        merged.append(pr)
    if not pr["closed"]:
        active.append(pr)

merged = sorted(merged, key=lambda item: (item["mergedAt"], item["url"]), reverse=True)
active = sorted(active, key=lambda item: (item["createdAt"], item["url"]), reverse=True)

print("merged:", "-"*80)
for item in merged:
    print(item["mergedAt"], item["url"])

print("active:", "-"*80)
for item in active:
    print(item["createdAt"], item["url"])
