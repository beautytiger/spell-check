from collections import defaultdict
from datetime import datetime, timedelta
import requests

url = "https://api.github.com/graphql"
prs = []


def get_github_token():
    path = "metadata/github-token.txt"
    file = open(path, "r")
    token = file.readline().strip()
    user = file.readline().strip()
    return user, token


github_id, api_token = get_github_token()


def get_all_prs(user_id=""):
    data = query_data(user_id)
    all_prs = data["data"]["user"]["pullRequests"]["nodes"]
    total_count = data["data"]["user"]["pullRequests"]["totalCount"]
    while data["data"]["user"]["pullRequests"]["pageInfo"]["hasNextPage"]:
        end_cursor = data["data"]["user"]["pullRequests"]["pageInfo"]["endCursor"]
        data = query_data(user_id=user_id, cursor=end_cursor)
        new_pr = data["data"]["user"]["pullRequests"]["nodes"]
        all_prs.extend(new_pr)
    assert len(all_prs) == total_count
    return all_prs


def query_data(user_id="", cursor=""):
    # , states: MERGED OPEN CLOSED
    # https://developer.github.com/v4/explorer/
    query = """
    {
      user(login: "%s") {
        pullRequests(%s) {
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

    first_page = "first: 100"
    next_page = 'first: 100, after: "%s"'
    if not cursor:
        input = first_page
    else:
        input = next_page % cursor
    req = query % (user_id, input)
    # https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line
    headers = {"Authorization": "token %s" % api_token}
    json = {"query": req}
    response = requests.post(url=url, json=json, headers=headers)
    return response.json()


prs = get_all_prs(github_id)


def localize_time(data):
    data["createdAt"] = datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)
    if data["closedAt"]:
        data["closedAt"] = datetime.strptime(data["closedAt"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)
    if data["mergedAt"]:
        data["mergedAt"] = datetime.strptime(data["mergedAt"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)


def clean_data():
    merged_pr = list()
    active_pr = list()
    mstat = defaultdict(int)
    astat = defaultdict(int)
    for pr in prs:
        localize_time(pr)
        if pr["merged"]:
            merged_pr.append(pr)
            mstat[pr["url"].split("/")[4]] += 1
        if not pr["closed"]:
            active_pr.append(pr)
            astat[pr["url"].split("/")[4]] += 1
    merged_pr = sorted(merged_pr, key=lambda item: (item["mergedAt"], item["url"]), reverse=True)
    active_pr = sorted(active_pr, key=lambda item: (item["createdAt"], item["url"]), reverse=True)
    return merged_pr, active_pr, dict(mstat), dict(astat)


merged, active, merged_stat, active_stat = clean_data()


def general_info():
    print("merged:", "-"*80)
    print("count:", len(merged))
    for item in merged:
        print(item["mergedAt"], item["url"])

    print("active:", "-"*80)
    print("count:", len(active))
    for item in active:
        print(item["createdAt"], item["url"])

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
        "virtual-kubelet",
        "notary",
        "opa",
        "node",
        "thanos",
        "typha",
        "envoy",
    }

    ignore_twice = {
        "jaeger",
        "spiffe",
        "linkerd2",
        "brigade",
        "kind",
        "OpenMetrics",
        "spec",
        "spire",
        "containerd",
        "pack",
        "flux",
        "openebs",
        "opentracing-go",
        "prometheus",
        "cni",
        "coredns",
        "opentelemetry-service",
        "telepresence",
        "virtual-kubelet",
        "notary",
    }

    todo_ignore = list()
    print("todo:", "-"*80)
    for p in all_projects:
        if p not in active_stat:
            if p not in ignore:
                print(p)
            else:
                todo_ignore.append(p)

    print("todo ignored:", "-"*80)
    for i in todo_ignore:
        if i not in ignore_twice:
            print(i)

    print("todo if you have time:", "-"*80)
    for i in todo_ignore:
        if i in ignore_twice:
            print(i)


def print_report():
    # range [16, 16)
    now = datetime.now()
    begin = "{}-{:02d}-16".format(now.year, now.month - 1)
    stop = "{}-{:02d}-16".format(now.year, now.month)
    begin = datetime.strptime(begin, "%Y-%m-%d")
    stop = datetime.strptime(stop, "%Y-%m-%d")
    report = list()
    for pr in merged:
        if begin < pr["mergedAt"] < stop:
            report.append(pr)
    report = sorted(report, key=lambda item: (item["url"], item["mergedAt"]), reverse=True)
    for item in report:
        print(item["mergedAt"], item["url"])
    print("count:", len(report))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print_report()
    else:
        general_info()
