from utils.color_print import color_print_file


def update_user_dict(word):
    pass


def run():
    file = "data/filetypo-kubernetes.txt"

    with open(file) as f:
        for line in f.readlines():
            path, words = line.strip().split(":")
            words = words.strip().split(" ")
            print(path)
            print(words)
            for word in words:
                color_print_file(path, [word, ])
                a = input()
                if a == "":
                    print("enter key")
                else:
                    print("key", a)


if __name__ == "__main__":
    run()
