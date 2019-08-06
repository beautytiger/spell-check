import os
from collections import defaultdict

from utils.helper import parse_words, clean_text, get_file_extension, get_comments, get_log_str, walk_dir
from utils.spell_checker import spell_check

from utils.passport import is_qualified_file


cache = dict()


TYPO_WORDS_FILE = "data/typos.txt"
TYPO_WORDS_BY_FILE = "output.txt"

spell = spell_check()


def run_spell_check(project=None):
    for file in walk_dir(project):
        if get_file_extension(file) not in ("go", ):
            continue
        if not is_qualified_file(file):
            continue
        parse_misspelled(file)


def get_text(file):
    with open(file, "r") as f:
        text = f.read()
    # comments = get_comments(text)
    logs = get_log_str(text)
    return logs


def parse_misspelled(file):
    raw_text = get_text(file)
    # print(file)
    # print("raw text:", raw_text)
    clear_text = clean_text(raw_text)
    # print("clean text:", clear_text)
    words = parse_words(clear_text)
    # print("words:", words)
    bad_words = spell.unknown(words)
    if not bad_words:
        return
    update_cache(file, bad_words)


def update_cache(file, bad_words):
    global cache
    cache[file] = bad_words


def print_cache(project="", file=""):
    global cache
    pro_len = len(project)
    if not project.endswith("/"):
        pro_len += 1
    output = defaultdict(list)
    for k, v in cache.items():
        output[len(v)].append((k, v))
    lens = sorted(list(output.keys()), reverse=True)
    if file:
        file = open(file, "w")
    for i in lens:
        if file:
            file.write("# {}\n".format(i))
        # print("#", i)
        for j in output[i]:
            out = "{path}:{line}:{row}: {short_code}: {message}".format(
                # path=j[0][pro_len:],
                path=j[0],
                line=0,
                row=0,
                short_code="TYPOS",
                message=" ".join(sorted(list(j[1]))),
            )
            if file:
                file.write(out+"\n")
            print(out)


def save_typo_words(file=""):
    global cache
    bad_words = set()
    for v in cache.values():
        bad_words = bad_words.union(v)
    result = list(bad_words)
    result.sort()
    with open(TYPO_WORDS_FILE, "w") as t:
        l = list()
        for i in result:
            l.append(i)
            if len(" ".join(l)) >= 80:
                t.write(" ".join(l) + "\n")
                l = list()
                continue
        else:
            t.write(" ".join(l) + "\n")


if __name__ == "__main__":
    # run_test()
    #
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-p", "--project", help="project path to scan", default="")
    # parser.add_argument(
    #     "-m",
    #     "--misspell",
    #     help="file of all misspelled words, default: typos.txt",
    #     default=TYPO_WORDS_FILE,
    # )
    # parser.add_argument(
    #     "-t",
    #     "--typofiles",
    #     help="file of all detected typos words, default: output.txt",
    #     default=TYPO_WORDS_BY_FILE,
    # )
    # args = parser.parse_args()
    #
    # # project = get_projects()
    # project = args.project
    # run_file_ext_statistics(project=project)
    project = "/home/matrix/workspace/github/kubernetes"
    run_spell_check(project=project)
    save_typo_words(file=TYPO_WORDS_BY_FILE)
    print_cache(project=project)
