import git
from utils.helper import timer, get_project


def main():
    for project in get_project():
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
