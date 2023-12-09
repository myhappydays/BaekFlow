import argparse
import pygetwindow
import json

with open('setting.json') as f:
    setting_data = json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", help="make new file.", action="store_true")
parser.add_argument("-s", "--submit", help="submit my file.", action="store_true")
parser.add_argument("-g", "--git", help="add and commit, push my file.", action="store_true")
args = parser.parse_args()

if args.new:

    active_window = pygetwindow.getAllTitles()

    browser_title = []

    for i in setting_data['browser']:
        for j in active_window:
            if j[len(j)-len(i):] == i:
                browser_title.append(j)

    print(browser_title)

    browser_window = pygetwindow.getWindowsWithTitle(browser_title[0])[0]
    browser_window.activate()
    
if args.submit:
    print("개발중입니다.")
if args.git:
    print("개발중입니다.")