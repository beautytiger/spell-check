
def format_dict():
    file = "metadata/words.dict"
    new_file = "metadata/new_words.dict"
    nf = open(new_file, "w")
    with open(file, "r") as f:
        words = f.read().split(" ")
    words.sort()
    cache = list()
    for idx, w in enumerate(words):
        if idx % 10 == 0:
            nf.write(" ".join(cache) + "\n")
            cache = list()
        cache.append(w)
    else:
        nf.write(" ".join(cache) + "\n")


if __name__ == "__main__":
    format_dict()