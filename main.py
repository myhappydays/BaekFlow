import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", help="make new file.", action="store_true")
parser.add_argument("-s", "--submit", help="submit my file.", action="store_true")
parser.add_argument("-g", "--git", help="add and commit, push my file.", action="store_true")
args = parser.parse_args()
if args.new:
    print("make file")
if args.submit:
    print("submit file")
if args.git:
    print("git file")