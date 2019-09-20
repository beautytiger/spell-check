from datetime import datetime, timedelta
import requests
import time

# https://stackoverflow.com/questions/17423598/how-can-i-get-a-list-of-all-pull-requests-for-a-repo-through-the-github-api
# You can get all pull requests (closed, opened, merged) through the variable state
# the default value for, "per_page=30". The maximum is per_page=100.
# To get more than 100 results, you need to call it multiple items: "&page=1", "&page=2"...
url_file = "prmark.txt"


def get_url():
    with open(url_file, "r") as f:
        url = f.read().strip()
    if url:
        return url
    return "https://api.github.com/repos/kubernetes/kubernetes/pulls?state=closed&direction=asc"


def save_url(url):
    with open(url_file, "w") as f:
        f.write(url)


# https://developer.github.com/v3/pulls/#get-a-single-pull-request
#   "created_at": "2011-01-26T19:01:12Z",
#   "updated_at": "2011-01-26T19:01:12Z",
#   "closed_at": "2011-01-26T19:01:12Z",
#   "merged_at": "2011-01-26T19:01:12Z",
def detail_info(pr_url):
    resp = requests.get(pr_url, auth=("beautytiger", "ethan@daocloud99"))
    print(resp.status_code)
    result = resp.json()
    line_tmp = "{html_url}|{title}|{loc}|{changed_files}|{additions}|{deletions}|{created_at}|{merged_at}\n"
    try:
        localize_time(result)
        line = line_tmp.format(
            html_url=result["html_url"],
            title=result["title"],
            loc=result["additions"] + result["deletions"],
            changed_files=result["changed_files"],
            additions=result["additions"],
            deletions=result["deletions"],
            created_at=result["created_at"],
            merged_at=result["merged_at"],
        )
        return line
    except (KeyError, TypeError):
        print(result)
        print(type(result))
        raise


def localize_time(data):
    data["created_at"] = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)
    data["merged_at"] = datetime.strptime(data["merged_at"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)


# sample return data
"""
{
  "html_url": "https://github.com/octocat/Hello-World/pull/1347",
  "state": "open",
  "title": "new-feature",
  "body": "Please pull these awesome changes",
  "labels": [
    {
      "id": 208045946,
      "node_id": "MDU6TGFiZWwyMDgwNDU5NDY=",
      "url": "https://api.github.com/repos/octocat/Hello-World/labels/bug",
      "name": "bug",
      "description": "Something isn't working",
      "color": "f29513",
      "default": true
    }
  ],
  "created_at": "2011-01-26T19:01:12Z",
  "updated_at": "2011-01-26T19:01:12Z",
  "closed_at": "2011-01-26T19:01:12Z",
  "merged_at": "2011-01-26T19:01:12Z",
  "merged": false,
  "comments": 10,
  "review_comments": 0,
  "maintainer_can_modify": true,
  "commits": 3,
  "additions": 100,
  "deletions": 3,
  "changed_files": 5
}
"""


def list_pr(url):
    print("current url:", url)
    save_url(url)
    resp = requests.get(url, auth=("beautytiger", "ethan@daocloud99"))
    print(resp.status_code)
    # print(resp.text)
    result = resp.json()
    # print(len(result))
    line = ""
    for r in result:
        if r["merged_at"]:
            single_url = r["url"]
            newline = detail_info(single_url)
            print(newline, end="")
            line += newline
    save_line(line)
    links = resp.headers.get("Link")
    links = links.split(",")
    link_next = link_last = None
    for link in links:
        if "next" in link:
            link_next = link
            link_next = link_next.split("<")[1].split(">")[0]
        elif "last" in link:
            link_last = link
            link_last = link_last.split("<")[1].split(">")[0]
    print("link_next", link_next)
    print("link_last", link_last)
    return link_next


def save_line(line):
    with open("k8s_pr.csv", "a") as f:
        f.write(line)


while True:
    try:
        url = get_url()
        while url:
            url = list_pr(url)
    except requests.exceptions.ConnectionError:
        print("connection error")
        time.sleep(10)
        print("restarting...")
        continue
