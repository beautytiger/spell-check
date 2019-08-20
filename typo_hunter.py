import json
import os
import sys

from utils.helper import parse_words, clean_text, \
    walk_dir, get_text, get_project_name, freq_get_file_name, save_all_typo_words, save_typo_by_file, \
    load_dict, get_unknown_words, load_user_dict, timer, pre_filter
from utils.spell_checker import spell_check


spell = spell_check()

user_dic = load_user_dict()


def spell_get_unknown_words(words):
    bad_words = spell.unknown(words)
    result = set()
    for w in bad_words:
        result.add(w.lower())
    return result


def load_word_freq(project):
    wfrq_cache = dict()
    allfrq_cache = dict()
    proj_name = get_project_name(project)
    try:
        with open(freq_get_file_name(proj_name), "r") as f:
            wfrq_cache = json.load(f)
    except Exception as e:
        print("json file empty: project %s" % e)
    try:
        with open(freq_get_file_name("all"), "r") as f:
            allfrq_cache = json.load(f)
    except Exception as e:
        print("json file empty: all %s" % e)
    return wfrq_cache, allfrq_cache


def get_all_words(file, level=2):
    """
    :param file: the target file to read
    :param level: return word level,
    2: code logging and error message
    3: 2 and code comment
    4: 3 and project document, markdown file etc.
    :return: list of words
    """
    raw_text = get_text(file, level=level)
    if not raw_text:
        return
    # print(file)
    # print("raw text:", raw_text)
    clear_text = clean_text(raw_text)
    # print("clean text:", clear_text)
    words = parse_words(clear_text)
    # print("words:", words)
    return words


@timer
def project_typo(project="", level=2):
    print(project)
    pro_freq, all_freq = load_word_freq(project)
    # cache is a dict storing file name as key and a list of typos as its value
    if os.path.isfile(project):
        gen = [project, ]
    else:
        gen = walk_dir(project)
    file_typo = dict()
    for file in gen:
        if not pre_filter(file, level=level):
            continue
        words = get_all_words(file, level=level)
        if not words:
            continue
        bad_words = spell_get_unknown_words(words)
        bad_words = get_unknown_words(bad_words, user_dic)
        result = list()
        for b in bad_words:
            b = b.lower()
            if pro_freq.get(b, 0) >= 8:
                # print("pass", b)
                continue
            if all_freq.get(b, 0) >= 24:
                # print("pass", b)
                continue
            result.append(b)
        if not result:
            continue
        file_typo[file] = result
    # save_all_typo_words(file_typo, project=project)
    save_typo_by_file(file_typo, project=project)


def all_project_typo(project="", level=2):
    with open("metadata/projects.txt", "r") as f:
        for line in f.readlines():
            path = line.strip()
            if path:
                if project:
                    if project == "all":
                        project_typo(path, level=level)
                    elif project in path.lower():
                        project_typo(path, level=level)
                else:
                    project_typo(path, level=level)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        all_project_typo(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) > 1:
        all_project_typo(sys.argv[1])
    else:
        all_project_typo()
