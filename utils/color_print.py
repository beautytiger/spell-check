#!/usr/bin/env python3
# 在终端上进行彩色打印
from termcolor import colored

from utils.helper import multi_find


def color_print_file(file, words=None, action=0):
    """
    :param file: 需要打印的文件路径
    :param words: 需要彩色显示的单词列表
    :param action: 0代表只高亮行打印， 1代表全文打印
    """
    with open(file, "r") as f:
        lines = f.readlines()
    for idx, s in enumerate(lines):
        color_print(s, words, action, idx+1)


def color_print(s, words=None, action=0, idx=0):
    s, colorable = color_string(s, words)
    if action == 0:
        if colorable:
            line = "{:<5d}: {}".format(idx, s)
            print(line, end="")
    else:
        line = "{:<5d}: {}".format(idx, s)
        print(line, end="")


# 这个方法在有重叠词时有bug
def color_string(s, words=None):
    cwords = color_words(words)
    slower = s.lower()
    index = list()
    colorable = False
    for word in words:
        ids = multi_find(slower, word)
        if ids:
            colorable = True
            for i in ids:
                index.append((i, i+len(word), word))
    if not colorable:
        return s, colorable
    index = sorted(index, key=lambda item: item[0], reverse=True)
    output = ""
    # print(s)
    # print(index)
    for start, end, word in index:
        output = cwords[word] + s[end:] + output
        s = s[:start]
        # print(output)
        # print(s)
    output = s + output
    return output, colorable


def color_words(words):
    result = dict()
    for w in words:
        result[w] = colored(w, 'red')
    return result


if __name__ == "__main__":
    color_print_file(
        "/home/matrix/workspace/github/kubernetes/staging/src/k8s.io/legacy-cloud-providers/azure/azure_test.go",
        words="expectected extected failt fouund insentive nuber serviceea servicesr unexpectected".split(),
        action=0
    )

    # color_print("""t.Errorf("Unexpectected error: %q", err)""", words=["unexpectected", "expectected"], action=0)
