import re

file = "/home/matrix/workspace/cncf/grpc/src/python/grpcio/grpc/framework/interfaces/face/face.py"
pattern_multiline = r"'(.*?)'"

text = open(file, "r").read()

print(re.findall(pattern_multiline, text, re.DOTALL))
