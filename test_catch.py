# test get text result
import sys
from utils.helper import clean_text, get_text


def parse_text(file, level=2):
    print(file, level)
    raw_text = get_text(file, level=level)
    print("raw text", "-"*80)
    print(raw_text)
    print("clean text", "-" * 80)
    clear_text = clean_text(raw_text)
    print(clear_text)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        parse_text(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) > 1:
        parse_text(sys.argv[1])
    else:
        print("error")
