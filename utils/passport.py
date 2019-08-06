

# 检测传入的文件是否值得检测，文件必须为绝对路径
def is_qualified_file(file=""):
    if not file:
        return False
    if not file.startswith("/"):
        return False
    # go项目，跳过go的包管理目录
    if "/vendor/" in file:
        return False
    # 跳过 .git 目录
    if "/.git/" in file:
        return False
    # 先跳过测试
    # if "test" in file:
    #     return False
    # if "staging" in file:
    #     return False
    return go_blacklist(file)


def go_blacklist(file=""):
    # kubernetes项目
    for i in [
        # kubernetes
        "kubectl/explain/formatter_test.go",
        "kubectl/explain/model_printer_test.go",
        "kubectl/explain/fields_printer_test.go",
        "/generated/",
        # go 测试文件，可跳过
        # "_test.go",

        # prometheus
        "assets_vfsdata.go",
        "MAINTAINERS",
        "/meetups",

        # etcd
        "etcd-dump-logs/README.md",
    ]:
        if i in file:
            return False
    return True
