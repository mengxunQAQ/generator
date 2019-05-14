import argparse

parser = argparse.ArgumentParser()
parser.add_argument("word", type=str, help="input word")

args = parser.parse_args()

print(args.word)