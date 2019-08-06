import re
import os

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


# golang的代码注释
pattern_comment = r"(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"  # /* comment */ or // comment
# 一般的代码打印语句
pattern_logging = r'\("(.*?)"'  # ("hello world"


# 返回文件的扩展名，小写
def get_file_extension(file):
    return os.path.splitext(file)[-1][1:].lower()


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


# 对字符串中不需要的pattern进行删除
def clean_text(string):
    # 替换一些常见的无效字符
    string = string.\
        replace("\n", " ").replace("\r", "").replace("\\n", " ").\
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


# 获取代码文件中的注释，适用于golang
def get_comments(text):
    comments = re.findall(pattern_comment, text, re.DOTALL)
    return " ".join(comments)


# 获取代码文件中的日志打印语句，适用于golang
def get_log_str(text):
    logs = re.findall(pattern_logging, text, re.DOTALL)
    return " ".join(logs)


# 接受一个绝对路径，返回绝对路径中的所有文件
def walk_dir(path):
    for dir, _, fnames in os.walk(path):
        for f in fnames:
            file = os.path.join(dir, f)
            yield file


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
