import try_nltk

from tokenize import tokenize, untokenize

sentence = open("/home/matrix/workspace/cncf/tuf/tuf/mirrors.py").read()

tokens = try_nltk.word_tokenize(sentence)

print(tokens)