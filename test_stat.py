# 对go测试文件的统计分析
import os

from datetime import datetime


def walk_dir(project):
    for dir, _, fnames in os.walk(project):
        for f in fnames:
            file = os.path.join(dir, f)
            if "/vendor/" in file:
                continue
            yield file


def get_file_extension(file):
    return os.path.splitext(file)[-1]


def check_file(file):
    test_file = file[:-3] + "_test.go"
    if check_exists(test_file):
        return True, get_line_num(file), get_line_num(test_file)
    return False, get_line_num(file), 0


def check_exists(file):
    return os.path.isfile(file)


def get_line_num(file):
    with open(file, "r") as f:
        for idx, l in enumerate(f):
            pass
    return idx + 1


def no_need_test(file):
    with open(file, "r") as f:
        for l in f.readlines():
            if l.startswith("func "):
                return False
    return True


def main(project=""):
    if not project.startswith("/"):
        return
    proj_str_len = len(project) if project.endswith("/") else len(project) + 1
    proj_name = project.split("/")[-1] if project.split("/")[-1] else project.split("/")[-2]
    no_test = list()
    have_test = list()
    for f in walk_dir(project):
        if not f.endswith(".go"):
            continue
        if f.endswith("test.go"):
            continue
        if no_need_test(f):
            continue
        exist, lc, tlc = check_file(f)
        f = f[proj_str_len:]
        if exist:
            have_test.append((f, lc, tlc))
        else:
            no_test.append((f, lc))
    print_no_test(no_test, proj_name)
    print_have_test(have_test, proj_name)


def get_file_name(name="", kind=""):
    now = datetime.now().strftime("%Y%m%d")
    return "data/test-{}-{}-{}.txt".format(name, kind, now)


def print_no_test(data, name=""):
    data = sorted(data, key=lambda item: (item[1], item[0]))
    lines = []
    print("no test go file:", "-"*20)
    for file, line_count in data:
        line = "{:<5d} {}".format(line_count, file)
        print(line)
        lines.append(line+"\n")
    with open(get_file_name(name, "notest"), "w") as output:
        output.writelines(lines)


def print_have_test(data, name=""):
    print("tested go file:", "-"*20)
    data = sorted(data, key=lambda item: (item[2], item[0]))
    lines = []
    for file, file_line_count, test_line_count in data:
        ratio = test_line_count / file_line_count
        line = "{:<5d} {:<6.2f} {:<5d} {}".format(test_line_count, ratio, file_line_count, file)
        print(line)
        lines.append(line+"\n")
    with open(get_file_name(name, "tested"), "w") as output:
        output.writelines(lines)


if __name__ == "__main__":
    main("/home/matrix/workspace/cncf/Dragonfly")
