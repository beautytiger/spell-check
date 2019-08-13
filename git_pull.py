import git
from utils.helper import timer


def main():
    with open("metadata/projects.txt", "r") as f:
        for line in f.readlines():
            project = line.strip()
            try:
                gitpull(project)
                print()
            except Exception as e:
                print(project)
                print(e)
                continue


@timer
def gitpull(path):
    g = git.cmd.Git(path)
    out = g.pull()
    print(path, "-" * 80)
    print(out)


if __name__ == "__main__":
    main()
