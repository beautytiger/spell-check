import json

from utils.helper import load_user_dict


user_dict = load_user_dict()


def load_word_freq():
    with open("metadata/freq-all.txt", "r") as f:
        allfrq_cache = json.load(f)
    return allfrq_cache


freq_dict = load_word_freq()

print("len of freq", len(freq_dict))
print("len of user", len(user_dict))

num = 0
for i in user_dict:
    count = freq_dict.get(i)
    if count:
        if count > 100:
            print("auto omit:", i)
            num += 1
    else:
        print("not in freq:", i)

print(num)
