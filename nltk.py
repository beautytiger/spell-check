import nltk

from tokenize import tokenize, untokenize

sentence = open("/home/matrix/workspace/github/tuf/tuf/mirrors.py").read()

tokens = nltk.word_tokenize(sentence)

print(tokens)