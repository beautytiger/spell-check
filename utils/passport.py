

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
        # 测试包，可跳过
        # "test",
        # go 测试文件，可跳过
        "_test.go",
        # 自动生成的changelog
        "CHANGELOG",
        "certs_test.go",
        "certs.go",
        "checks_test.go",
        "certificates.go",
        "x509_test.go",
        "certificate_manager_test.go",
        "update_owners.py",
        "printer_test.go",
        "secret_for_tls_test.go",
        "key_test.go",
        "storageversionhashdata/data.go",

        # from go lint file
        "zz_generated",
        "generated.pb.go",
        "generated.proto",
        "types_swagger_doc_generated.go",

        # prometheus
        "assets_vfsdata.go",
        "MAINTAINERS",
        "RELEASE",
        "/meetups",

        # etcd
        "etcd-dump-logs/README.md",

        # helm
        "CONTRIBUTING",

        "AUTHORS.md",
        "History.md",
        "HISTORY.md",
    ]:
        if i in file:
            return False
    return True
