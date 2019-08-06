import json
from collections import defaultdict
from datetime import datetime

from utils.helper import parse_words, clean_text, get_file_extension, get_comments, get_log_str, walk_dir, get_text, get_project_name, freq_get_file_name
from utils.spell_checker import spell_check

from utils.passport import is_qualified_file
from utils.color_print import color_print_file

cache = dict()

wfrq = defaultdict(int)

wfrq_cache = dict()
allfrq_cache = dict()


TYPO_WORDS_FILE = "data/typos.txt"
TYPO_WORDS_BY_FILE = "output.txt"

spell = spell_check()


def load_word_freq(project):
    global wfrq_cache, allfrq_cache
    proj_name = get_project_name(project)
    with open(freq_get_file_name(proj_name), "r") as f:
        try:
            wfrq_cache = json.load(f)
        except json.decoder.JSONDecodeError:
            print("json file empty: project")
    with open(freq_get_file_name("all"), "r") as f:
        try:
            allfrq_cache = json.load(f)
        except json.decoder.JSONDecodeError:
            print("json file empty: all")


def run_spell_check(project=None, stat=False):
    load_word_freq(project)
    for file in walk_dir(project):
        # 进行词频统计
        parse_misspelled(file)


def parse_misspelled(file):
    raw_text = get_text(file)
    if not raw_text:
        return
    # print(file)
    # print("raw text:", raw_text)
    clear_text = clean_text(raw_text)
    # print("clean text:", clear_text)
    words = parse_words(clear_text)
    # print("words:", words)
    bad_words = spell.unknown(words)
    bad_words = filter_bad_words(bad_words)
    if not bad_words:
        return
    update_cache(file, bad_words)


def filter_bad_words(bad_words):
    result = list()
    for b in bad_words:
        b = b.lower()
        if wfrq_cache.get(b, 0) >= 5:
            # print("pass", b)
            continue
        if allfrq_cache.get(b, 0) >= 10:
            # print("pass", b)
            continue
        result.append(b)
    return result


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
            # color_print_file(j[0], j[1])
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
    # project = "/home/matrix/workspace/github/kubernetes"
    # project = "/home/matrix/workspace/github/minikube"
    # project = "/home/matrix/workspace/github/prometheus"
    # project = "/home/matrix/workspace/github/helm"
    # project = "/home/matrix/workspace/github/vitess"
    # project = "/home/matrix/workspace/github/kops"
    # project = "/home/matrix/workspace/github/rook"
    project = "/home/matrix/workspace/github/etcd"
    # project = "/home/matrix/workspace/github/rkt"
    # project = "/home/matrix/workspace/github/kubespray"
    # project = "/home/matrix/workspace/github/tuf"
    run_spell_check(project=project)
    save_typo_words(file=TYPO_WORDS_BY_FILE)
    print_cache(project=project)
