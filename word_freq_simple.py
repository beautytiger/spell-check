# 对代码进行简单的分词，统计词频
import simplejson
from utils.helper import get_project
from collections import defaultdict

from utils.helper import parse_raw_words, get_text_simple, walk_dir, get_project_name, freq_simple_get_file_name, timer


def project_word_freq():
    allfrq = defaultdict(int)
    for path in get_project():
        print(path)
        data = get_word_frequency(path)
        for i in data:
            allfrq[i] += data[i]
    data = simplejson.dumps(allfrq, indent=4, item_sort_key=lambda i: (-i[1], i[0]))
    with open(freq_simple_get_file_name("all"), "w") as f:
        f.write(data)


@timer
def get_word_frequency(project=""):
    wfrq = defaultdict(int)
    for file in walk_dir(project):
        raw_text = get_text_simple(file)
        words = parse_raw_words(raw_text)
        for word in words:
            wfrq[word] += 1
    proj_name = get_project_name(project)
    data = simplejson.dumps(wfrq, indent=4, item_sort_key=lambda i: (-i[1], i[0]))
    with open(freq_simple_get_file_name(proj_name), "w") as f:
        f.write(data)
    return wfrq


if __name__ == "__main__":
    project_word_freq()
