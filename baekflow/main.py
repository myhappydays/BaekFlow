import argparse
import pygetwindow
import json
import pyautogui
import clipboard
import time
import os
import webbrowser

def load_settings():
    # 설정 파일을 읽어서 반환
    with open('baekflow\setting\setting.json') as f:
        return json.load(f)

def get_browser_title(setting_data):
    # 현재 열려있는 창 중 브라우저 창을 식별하여 리스트로 반환
    active_window = pygetwindow.getAllTitles()
    browser_title = []

    for i in setting_data['browser']:
        for j in active_window:
            if j.endswith(i):
                browser_title.append(j)

    return browser_title

def get_browser_url(browser_title, setting_data):
    # 각 브라우저 창에서 URL을 찾아 리스트로 반환
    site_url = []
    site_title = []

    for title in browser_title:
        temp_windows = pygetwindow.getWindowsWithTitle(title)[0]
        browser_window = temp_windows
        browser_window.activate()
        time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'c')
        browser_url = clipboard.paste()

        for i, temp_url in enumerate(setting_data['site url']):
            if temp_url in browser_url:
                site_url.append(browser_url)
                site_title.append(title)

    return site_url, site_title

def create_file_name(number, name, setting_data):
    file_name = ""

    for j in setting_data['file name']:
        if j == 'number':
            file_name += number
        elif j == 'name':
            file_name += name
        else:
            file_name += j

    return file_name

def create_file(site_url, site_title, setting_data):
    # 각 사이트에 대해 파일을 생성
    for i, url in enumerate(site_url):
        # 문제 번호 추출
        number = url.split('/')[-1][::-1]
        number = number[::-1]

        # 문제 이름 추출
        name = site_title[i].split("번: ")[1].split(" - Whale")[0]

        # 설정된 파일 이름 생성
        file_name = create_file_name(number, name, setting_data)

        file_path = setting_data['path'] + file_name + setting_data['programing language']
        ide_cmd = setting_data['ide']

        print(file_path)
        with open(file_path, 'w'):
            pass

        open_ide = os.popen(f'{ide_cmd} {file_path}').read()
        print(open_ide)

def submit_code(site_url, site_title, setting_data):
    # 코드를 제출하는 함수
    for i, url in enumerate(site_url):
        # 문제 번호 추출
        number = url.split('/')[-1][::-1]
        number = number[::-1]

        # 문제 이름 추출
        name = site_title[i].split("번: ")[1].split(" - Whale")[0]

        # 설정된 파일 이름 생성 
        file_name = create_file_name(number, name, setting_data)

        file_path = setting_data['path'] + file_name + setting_data['programing language']
        with open(file_path, 'r') as f:
            code = f.read()

        clipboard.copy(code)

        print(setting_data['submit url'] + number)
        webbrowser.open(setting_data['submit url'] + number)

        time.sleep(2)

        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('ctrl', 'enter')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new", help="Create a new file.", action="store_true")
    parser.add_argument("-s", "--submit", help="Submit a file.", action="store_true")
    parser.add_argument("-g", "--git", help="Add, commit, and push files.", action="store_true")
    args = parser.parse_args()

    setting_data = load_settings()
    browser_title = get_browser_title(setting_data)

    if args.new:
        if browser_title:
            site_url, site_title = get_browser_url(browser_title, setting_data)
            if site_url:
                create_file(site_url, site_title, setting_data)
            else:
                print("Error: Not the specified page.")
        else:
            print("Error: Browser is not open.")

    if args.submit:
        if browser_title:
            site_url, site_title = get_browser_url(browser_title, setting_data)
            if site_url:
                submit_code(site_url, site_title, setting_data)

    if args.git:
        print("개발 중입니다.")
