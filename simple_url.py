import re

pattern = r"\(https://.*?\)"

file = "/home/matrix/go/src/k8s.io/kubernetes/CHANGELOG-1.16.md"
with open(file) as f:
    lines = f.read()
    urls = re.findall(pattern, lines)

new_set = set()
for u in urls:
    if "kubernetes/kubernetes" in u:
        if u in new_set:
            print(u)
        else:
            new_set.add(u)
