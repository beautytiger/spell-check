# test get text result
import sys
from utils.helper import get_text, pre_filter, get_project
from utils.helper import walk_dir, timer


def parse_text(file, level=2):
    print(file, level)
    raw_text = get_text(file, level=level)
    # print("raw text", "-"*80)
    print(raw_text)
    # print("clean text", "-" * 80)
    # clear_text = clean_text(raw_text)
    # print(clear_text)


@timer
def project_typo(project="", level=2):
    print(project)
    gen = walk_dir(project)
    for file in gen:
        if not pre_filter(file, level=level):
            continue
        parse_text(file, level=level)
        print(file)
        a = input()


def all_project_typo(project="", level=2):
    for path in get_project():
        if project:
            if project in path.lower():
                project_typo(path, level=level)
        else:
            project_typo(path, level=level)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 2:
        all_project_typo(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) > 1:
        parse_text(sys.argv[1])
    else:
        all_project_typo()
