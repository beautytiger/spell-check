from collections import defaultdict

from utils.helper import get_file_extension, walk_dir, print_freq_dict
from utils.passport import is_qualified_file


def run_file_ext_statistics(project, cache):
    if not project:
        return
    statistics = defaultdict(int)
    for file in walk_dir(project):
        if not is_qualified_file(file):
            continue
        ext = get_file_extension(file)
        # 看看没有扩展名的文件都是些啥，没发现什么有价值的
        # if not ext:
        #     print(file)
        statistics[ext] += 1
        cache[ext] += 1
    print(project)
    print_freq_dict(data=statistics)


def main():
    cache = defaultdict(int)
    with open("metadata/projects.txt", "r") as f:
        for line in f.readlines():
            path = line.strip()
            if path:
                run_file_ext_statistics(path, cache=cache)
    print("ALL")
    print_freq_dict(cache)


if __name__ == "__main__":
    main()
