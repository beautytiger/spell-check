#!/usr/bin/env python3
# 在终端上进行彩色打印
from termcolor import colored


# 返回字符串s包含字符串t的首坐标列表
def multi_find(s, t, trunc=0):
    if (not s) or (not t):
        return []
    result = list()
    loc = s.find(t)
    if loc == -1:
        return []
    else:
        result.append(loc+trunc)
        result.extend(multi_find(s[loc+len(t):], t, trunc=loc+len(t)+trunc))
    return result


def color_print_file(file, words=None, action=0):
    with open(file, "r") as f:
        lines = f.readlines()
    for idx, s in enumerate(lines):
        color_print(s, words, action, idx+1)


def color_print(s, words=None, action=0, idx=0):
    s, colorable = color_string(s, words, action)
    if colorable:
        line = "{:<5d}: {}".format(idx, s)
        print(line, end="")


def color_string(s, words=None, action=0):
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
        result[w] = colored(w, 'yellow')
    return result


if __name__ == "__main__":
    # color_print_file(
    #     "/home/matrix/workspace/github/kubernetes/staging/src/k8s.io/legacy-cloud-providers/azure/azure_test.go",
    #     words="expectected extected failt fouund insentive nuber serviceea servicesr unexpectected".split()
    # )
    color_print("""t.Errorf("Unexpectected error: %q", err)""", words=["unexpectected", "expectected"], action=0)