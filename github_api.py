from collections import defaultdict
from datetime import datetime, timedelta
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


def localize_time(data):
    data["createdAt"] = datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)
    if data["closedAt"]:
        data["closedAt"] = datetime.strptime(data["closedAt"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)
    if data["mergedAt"]:
        data["mergedAt"] = datetime.strptime(data["mergedAt"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)


merged = list()
active = list()
for pr in prs:
    localize_time(pr)
    if pr["merged"]:
        merged.append(pr)
    if not pr["closed"]:
        active.append(pr)

merged = sorted(merged, key=lambda item: (item["mergedAt"], item["url"]), reverse=True)
active = sorted(active, key=lambda item: (item["createdAt"], item["url"]), reverse=True)

merged_stat = defaultdict(int)
active_stat = defaultdict(int)

print("merged:", "-"*80)
for item in merged:
    print(item["mergedAt"], item["url"])
    merged_stat[item["url"].split("/")[4]] += 1

print("active:", "-"*80)
for item in active:
    print(item["createdAt"], item["url"])
    active_stat[item["url"].split("/")[4]] += 1

print("merged stats:", "-"*80)
print(dict(merged_stat))

print("active:", "-"*80)
print(dict(active_stat))

all_projects = set()
with open("metadata/projects.txt") as f:
    for line in f.readlines():
        all_projects.add(line.strip().split("/")[-1])

ignore = {
    "falco",
    "spire",
    "telepresence",
    "nats-server",
    "cni",
    "kubespray",
    "openebs",
    "kubeadm",
    "spiffe",
    "spec",
    "pack",
    "opentracing-go",
    "OpenMetrics",
    "tuf",
    "flux",
    "brigade",
    "etcd",
    "kind",
    "prometheus",
    "containerd",
    "jaeger",
    "cri-o",
    "coredns",
    "linkerd2",
    "opentelemetry-service",
}
print("todo:", "-"*80)
for p in all_projects:
    if p not in active_stat and p not in ignore:
        print(p)
