import argparse
import pygetwindow
import json
import pyautogui
import clipboard
import time
import os
import webbrowser

with open('baekflow\setting\setting.json') as f:                                                                     #세팅파일 불러오기
        setting_data = json.load(f)

browser_title = []
site_url = []

def get_browser_title():
    active_window = pygetwindow.getAllTitles()                                                      #현재 열려있는 창 불러오기

    for i in setting_data['browser']:                                                               #브라우저 창 분류
        for j in active_window:
            if j[len(j)-len(i):] == i:
                browser_title.append(j)
    
    print(browser_title)

def get_browser_url():
    for i in range(len(browser_title)):
        browser_window = pygetwindow.getWindowsWithTitle(browser_title[i])[0]
        print(pygetwindow.getWindowsWithTitle(browser_title[i])[0])
        browser_window.activate()                                                                       #브라우저 창 포커스

        time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')                                                                   #url 복사

        browser_url = clipboard.paste()

        print("browser_url", browser_url)
                
        for i in range(len(setting_data['site url'])):                                                  #특정 사이트 url 분류
            temp_url = setting_data['site url'][i]
            if temp_url in browser_url:
                site_url.append(browser_url)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new", help="make new file.", action="store_true")
    parser.add_argument("-s", "--submit", help="submit my file.", action="store_true")
    parser.add_argument("-g", "--git", help="add and commit, push my file.", action="store_true")
    args = parser.parse_args()

    if args.new:
        
        get_browser_title()

        if len(browser_title) != 0:

            get_browser_url()

            if len(site_url) != 0:
                for i in site_url:
                    print("site_url", i)
                    number = ""
                    for i in i[::-1]:                                                                           #문제 번호 추출
                        if i != '/':
                            number += i
                        else:
                            break
                    number = number[::-1]

                    file_name = ""

                    for i in setting_data['file name']:
                        if i == 'number':
                            file_name += number

                    file_path = setting_data['path']+file_name+setting_data['programing language']
                    ide_cmd = setting_data['ide']

                    print(file_path)                                                                                #파일 만들기
                    f = open(file_path, 'w')
                    f.close()

                    open_ide = os.popen(f'{ide_cmd} {file_path}').read()                                           #open ide
                    print(open_ide)
            
            else:
                print("Error: Not the specified page.")

        else:
            print("Error: Browser is not open.")

    if args.submit:
        get_browser_title()

        if len(browser_title) != 0:

            get_browser_url()

            if len(site_url) != 0:

                for i in site_url:
                    print("site_url", i)
                    number = ""
                    for i in i[::-1]:                                                                           #문제 번호 추출
                        if i != '/':
                            number += i
                        else:
                            break
                    number = number[::-1]

                    file_name = ""

                    for i in setting_data['file name']:
                        if i == 'number':
                            file_name += number

                    file_path = setting_data['path']+file_name+setting_data['programing language']
                    f = open(file_path, 'r')

                    code = ""

                    while True:
                        c = f.read()
                        if c == '':
                            break
                        code += c

                    clipboard.copy(code)

                    print(setting_data['submit url'] + number)
                    webbrowser.open(setting_data['submit url'] + number)

                    time.sleep(2)

                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('ctrl', 'enter')

    if args.git:
        print("개발중입니다.")