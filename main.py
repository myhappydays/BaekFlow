import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="제곱해드림.", type=int)
args = parser.parse_args()
print(args.square**2)