import git

with open("data/projects.txt", "r") as f:
    lines = f.readlines()

for l in lines:
    path = l.strip()
    if path:
        g = git.cmd.Git(path)
        out = g.pull()
        print(path)
        print(out)
