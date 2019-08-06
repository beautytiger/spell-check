

def get_projects(project="kubernetes"):
    # kubernetes prometheus helm envoy fluentd coredns containerd tikv etcd
    return os.path.join("/home/matrix/workspace/github", project)


def run_test():
    text = get_text("test.go")
    # print(text)
    text = clean_text(text)
    # print(text)

