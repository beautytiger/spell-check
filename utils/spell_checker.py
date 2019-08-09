from spellchecker import SpellChecker

KNOWN_WORDS_FILE = "data/words1.txt"


def spell_check():
    checker = SpellChecker()
    # w = list()
    # try:
    #     with open(KNOWN_WORDS_FILE) as f:
    #         for line in f.readlines():
    #             if line.startswith("#"):
    #                 continue
    #             w.extend(line.strip().split())
    #     # 载入非错误单词（手工认证）
    #     checker.word_frequency.load_words(w)
    # except Exception as e:
    #     print(e)
    return checker


