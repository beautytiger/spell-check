import re

# file = "/home/matrix/workspace/cncf/spire/api/workload/x509_client.go"
# pattern_multiline = r'(import \(.*?\))'

# text = open(file, "r").read()

# print(re.findall(pattern_multiline, text, re.DOTALL))

# text = re.sub(pattern_multiline, " ", text, flags=re.DOTALL)
# print(text)

print(re.findall(r"\w+", " },"))
