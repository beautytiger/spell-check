import re

pattern_word = r"\b\w+\b"
pattern_contain_num = r".*\d.*"
pattern_camelcase = r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)"  # helloWorld

# https://stackoverflow.com/questions/19021873/upper-and-lower-camel-case
pattern_upper_camelcase = r"[A-Z]+[a-z0-9]*[A-Z0-9]+[a-z0-9]+[A-Za-z0-9]*"
pattern_lower_camelcase = r"[a-z]+[A-Z0-9]+[a-z0-9]+[A-Za-z0-9]*"


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


# 解析字符串中的单词
def parse_words(string):
    raw_words = parse_raw_words(string)
    clean_words = tidy_words(raw_words)
    words = parse_camelcase(clean_words, drop=True)
    return words


# 解析字符串中的原始单词
def parse_raw_words(string):
    raw_words = re.findall(pattern_word, string)
    return raw_words


# 删除单词列表中无意义的词
def tidy_words(raw_words):
    words = list()
    for w in raw_words:
        # 跳过长度太短的词
        if len(w) <= 2:
            continue
        # 跳过带连字符或者包含数字的词
        if "_" in w or re.match(pattern_contain_num, w):
            continue
        words.append(w)
    return words


# 解析驼峰单词，删除或者分解
def parse_camelcase(words, drop=True):
    result = list()
    if drop:
        for w in words:
            if re.match(pattern_upper_camelcase, w) or re.match(pattern_lower_camelcase, w):
                continue
            result.append(w)
    else:
        for w in words:
            word_list = re.findall(pattern_camelcase, w)
            result.extend(word_list)
    return result


if __name__ == "__main__":
    cc = [
        "Wordtoolong",
        "wordtoolong",
        "camelcase",
        "CamelCase",
        "camelCase",
        "CCamelCase",
        "CamelCCase",
        "CCamelCCase",
        "CAMELCase",
    ]
    print(cc)
    print(parse_camelcase(cc))
