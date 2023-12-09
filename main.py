import argparse
import pygetwindow
import json
import pyautogui
import clipboard

with open('setting.json') as f:                                                                     #세팅파일 불러오기
    setting_data = json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", help="make new file.", action="store_true")
parser.add_argument("-s", "--submit", help="submit my file.", action="store_true")
parser.add_argument("-g", "--git", help="add and commit, push my file.", action="store_true")
args = parser.parse_args()

if args.new:

    active_window = pygetwindow.getAllTitles()                                                      #현재 열려있는 창 불러오기

    browser_title = []

    for i in setting_data['browser']:                                                               #브라우저 창 분류
        for j in active_window:
            if j[len(j)-len(i):] == i:
                browser_title.append(j)

    print(browser_title)

    browser_window = pygetwindow.getWindowsWithTitle(browser_title[0])[0]
    browser_window.activate()                                                                       #브라우저 창 포커스

    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'c')                                                                   #url 복사

    browser_url = clipboard.paste()

    site_url = []
    
    for i in range(len(setting_data['site url'])):
        temp_url = setting_data['site url'][i]
        if temp_url in browser_url:
            site_url.append(temp_url)

if args.submit:
    print("개발중입니다.")
if args.git:
    print("개발중입니다.")