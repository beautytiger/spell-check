import os
import sys

from utils.color_print import color_print_file


def get_target_file(file=""):
    files = os.listdir("data")
    for f in files:
        if not f.startswith("filetypo-"):
            continue
        if file in f:
            return "data/{}".format(f)
    return ""


def run(file=""):
    file = get_target_file(file=file)
    if not file:
        print("file not exists")
        return
    print(file)
    with open(file) as f:
        for line in f.readlines():
            if not line.startswith("/"):
                continue
            path, words = line.strip().split(":")
            words = words.strip().split(" ")
            print()
            print(path)
            color_print_file(path, words)
            print(path)
            print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("no project specified")
