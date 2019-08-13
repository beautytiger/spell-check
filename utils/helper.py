import re
import os
import time
from collections import defaultdict
import git
from datetime import datetime

from .passport import is_qualified_file

pattern_word = r"\b\w+\b"
pattern_contain_num = r".*\d.*"
pattern_camelcase = r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)"  # helloWorld

# https://stackoverflow.com/questions/19021873/upper-and-lower-camel-case
pattern_upper_camelcase = r"[A-Z]+[a-z0-9]*[A-Z0-9]+[a-z0-9]+[A-Za-z0-9]*"
pattern_lower_camelcase = r"[a-z]+[A-Z0-9]+[a-z0-9]+[A-Za-z0-9]*"

# 常见的可删除字符串
pattern_url = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
pattern_note = r"@\w+"  # @yourname
pattern_num = r"#\w+"  # #yourname
pattern_todo = r"TODO\(.*\)"  # TODO(mkwiek)
pattern_email = r"([\w\.-]+@[\w\.-]+\.[\w]+)"
pattern_repeat = r'(.)\1\1\1\1*'
pattern_go_import = r'(import \(.*?\))'
pattern_go_const = r'(const \(.*?\n\)\n)'
pattern_go_const_oneline = r'(const.*?\n)'
pattern_c_include = r'(#include.*?\n)'

# golang的代码注释
pattern_comment = r"(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"  # /* comment */ or // comment
# 一般的代码打印语句
pattern_logging = r'"(.*?)"'
pattern_logging_single = r"'(.*?)'"
pattern_multiline = r'`.*?`'
pattern_multiline_python = r'"""(.*?)"""'

READABLE = ("go", "py", "cc", "rb", "rs", "md")
SOURCE =   ("go", "py", "cc", "rb", "rs")


# 无任何异常处理，十分脆弱，轻拿轻用
def get_project_file_prefix(project=""):
    g = git.cmd.Git(project)
    result = g.remote(verbose=True)
    project_url = result.split(" ")[0].split("\t")[1]
    if project_url.endswith(".git"):
        project_url = project_url[:-4]
    file_prefix = "/blob/master/"
    return project_url + file_prefix


def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        result = func(*args, **kwargs)
        after = time.time()
        print("time cost: {:.3f}".format(after-before))
        return result
    return wrapper


def load_dict():
    file = "metadata/words.dict"
    with open(file, "r") as f:
        words = f.read().split(" ")
    dic = set(words)
    return dic


def load_user_dict():
    file = "metadata/user.dict"
    words = list()
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            if not line:
                continue
            words += line.split(" ")
    dic = set(words)
    return dic


def get_unknown_words(words, dic):
    result = set()
    for word in words:
        lw = word.lower()
        if lw not in dic:
            result.add(lw)
    return result


# 返回文件的扩展名，小写
def get_file_extension(file):
    return os.path.splitext(file)[-1][1:].lower()


# 解析字符串中的单词
def parse_words(string):
    raw_words = parse_raw_words(string)
    clean_words = tidy_words(raw_words)
    words = parse_camelcase(clean_words, drop=False)
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


# 对字符串中不需要的pattern进行删除
def clean_text(string):
    # 替换一些常见的无效字符
    string = string.\
        replace("\n", " ").replace("\r", "").replace("\\n", " ").replace("\\t", " ").\
        replace("%s", " ").replace("%v", " ").replace("%q", " ")
    # email
    string = re.sub(pattern_email, "", string)
    # print(re.findall(pattern_email, string))
    # 删除url
    string = re.sub(pattern_url, "", string)
    # 删除@someone这种格式的人名
    string = re.sub(pattern_note, "", string)
    # 删除#someone这种格式的人名
    string = re.sub(pattern_num, "", string)
    # 删除TODO(someone)这种格式的人名
    string = re.sub(pattern_todo, "", string)
    # repeat
    # print(re.findall(pattern_repeat, string))
    string = re.sub(pattern_repeat, " ", string)
    return string


# 获取代码文件中的注释，适用于golang, cpp, c
def get_comments(text):
    comments = re.findall(pattern_comment, text, re.DOTALL)
    return " ".join(comments)


# 获取代码文件中的日志打印语句，适用于golang, python
def get_log_str(text):
    logs = re.findall(pattern_logging, text, re.DOTALL)
    # logs += re.findall(pattern_logging_single, text, re.DOTALL)
    logs += re.findall(pattern_multiline, text, re.DOTALL)
    # logs += re.findall(pattern_multiline_python, text, re.DOTALL)
    return " ".join(logs)


# 接受一个绝对路径，返回绝对路径中的所有文件
def walk_dir(path):
    for dir, _, fnames in os.walk(path):
        for f in fnames:
            file = os.path.join(dir, f)
            yield file


def print_freq_dict(data, top=20):
    stat = [(k, v) for k, v in data.items()]
    stat = sorted(stat, key=lambda i: i[1], reverse=True)
    for idx, i in enumerate(stat):
        # 只打印top20的文件
        if idx >= top:
            break
        print("{:>20s}: {:<4d}".format(i[0], i[1]))


def pre_clean(text, ext=""):
    # go import
    text = re.sub(pattern_go_import, " ", text, flags=re.DOTALL)
    # go const, notice this will kill comment in const block
    text = re.sub(pattern_go_const, " ", text, flags=re.DOTALL)
    if ext == "go":
        text = re.sub(pattern_go_const_oneline, " ", text, flags=re.DOTALL)
    # 与上面的go const略有冲突
    text = re.sub(pattern_c_include, " ", text)
    return text


def pre_filter(file, level=2):
    ext = get_file_extension(file)
    if ext not in READABLE:
        return False
    if file.endswith(".pb.go"):
        return False
    if file.endswith("_test.go"):
        return False
    if file.endswith("keystoretest/keymap.go"):
        return False
    if file.endswith("mysql/constants.go"):
        return False
    if file.endswith("boringssl/crypto_test_data.cc"):
        return False
    if file.endswith("end2end/tests/hpack_size.cc"):
        return False
    if file.endswith("gen_assets.go"):
        return False
    if "/vendor/" in file:
        return False
    if "/node_modules/" in file:
        return False
    if ext == "md" and level <= 3:
        return False
    return True


def get_text(file, get_all=False, level=2):
    if os.path.islink(file):
        return ""
    ext = get_file_extension(file)
    if ext not in READABLE:
        return ""
    with open(file, "r") as f:
        text = f.read()
        text = pre_clean(text, ext=ext)
    if get_all:
        return text
    # 词频统计可以包含任意合法文件
    if not is_qualified_file(file):
        return ""
    if ext in SOURCE:
        if level >= 3:
            comments = get_comments(text)
        else:
            comments = " "
        logs = get_log_str(text)
        return comments + " " + logs
    if ext == "md" and level >= 4:
        return text
    return ""


def get_project_name(project=""):
    if project.endswith("/"):
        return project.split("/")[-2].lower()
    else:
        return project.split("/")[-1].lower()


def freq_get_file_name(name=""):
    now = datetime.now().strftime("%Y%m%d")
    # return "data/freq-{}-{}.txt".format(name, now)
    return "metadata/freq-{}.txt".format(name)


def alltypo_get_file_name(name=""):
    now = datetime.now().strftime("%Y%m%d")
    # return "data/freq-{}-{}.txt".format(name, now)
    return "data/alltypo-{}.txt".format(name)


def filetypo_get_file_name(name=""):
    now = datetime.now().strftime("%Y%m%d")
    # return "data/freq-{}-{}.txt".format(name, now)
    return "data/filetypo-{}.txt".format(name)


def save_typo_by_file(data, project=""):
    url_prefix = get_project_file_prefix(project)
    pro_name = get_project_name(project)
    file_name = filetypo_get_file_name(pro_name)
    file = open(file_name, "w")
    output = defaultdict(list)
    for k, v in data.items():
        output[len(v)].append((k, v))
    lens = sorted(list(output.keys()), reverse=True)
    for i in lens:
        for j in output[i]:
            # color_print_file(j[0], j[1])
            # out = "{path}:{line}:{row}: {short_code}: {message}".format(
            #     path=j[0],
            #     line=0,
            #     row=0,
            #     short_code="TYPOS",
            #     message=" ".join(sorted(list(j[1]))),
            # )
            out = "{path}:  {message}".format(
                path=j[0],
                message=" ".join(sorted(list(j[1]))),
            )
            print(out)
            file.write(out + "\n")
            file_url = url_prefix + j[0][len(project)+1:]
            file.write(file_url + "\n")


def save_all_typo_words(data, project=""):
    pro_name = get_project_name(project)
    file_name = alltypo_get_file_name(pro_name)
    bad_words = set()
    for v in data.values():
        bad_words = bad_words.union(v)
    result = list(bad_words)
    result.sort()
    with open(file_name, "w") as t:
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
