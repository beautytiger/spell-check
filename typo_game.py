import signal
import sys
import os

from utils.color_print import color_print_file

cache = set()
full_cache = set()

fd = open("metadata/tmpdict.txt", "a")


def receive_signal(signum, stack):
    print('prepare to exiting...')
    before_exit()
    sys.exit()


# Register signal handlers
signal.signal(signal.SIGINT, receive_signal)


def update_user_dict(word):
    global cache
    cache.add(word)
    full_cache.add(word)
    if len(cache) >= 8:
        fd.write(" ".join(cache) + "\n")
        cache = set()
    return


def before_exit():
    print("final saving")
    global cache
    if cache:
        fd.write(" ".join(cache) + "\n")


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
            print(path)
            print(words)
            for word in words:
                if word in full_cache:
                    continue
                color_print_file(path, [word, ])
                a = input()
                # a word that is right
                if a == "":
                    update_user_dict(word)
                    print("record to dict:", word)
                # a word that worth a pr
                else:
                    print("bad word: ", word)
    before_exit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("no project specified")
