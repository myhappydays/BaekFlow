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

    print(f'browser title: {browser_title}')
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

    print(f'site url: {site_url}')
    print(f'site title: {site_title}')
    return site_url, site_title

def create_name(number, name, setting_data):
    file_name = ""

    for j in setting_data['file name']:
        if j == 'number':
            file_name += number
        elif j == 'name':
            file_name += name
        else:
            file_name += j

    print(f'file name: {file_name}')
    return file_name

def get_question_information(url, title):
    # 문제 번호 추출
    number = url.split('/')[-1][::-1]
    number = number[::-1]

    # 문제 이름 추출
    name = title.split("번: ")[1].split(" - Whale")[0]

    return number, name

def create_file_path(url, title, setting_data):
    # 각 사이트에 대해 파일 경로 생성

    number, name = get_question_information(url, title)

    # 설정된 파일 이름 생성
    file_name = create_name(number, name, setting_data)

    file_path = setting_data['path'] + file_name + setting_data['programing language']
    
    return file_path

def create_file(site_url, site_title, setting_data):
    # 각 사이트에 대해 파일을 생성
    for i, url in enumerate(site_url):
        file_path = create_file_path(url, site_title[i], setting_data)
        ide_cmd = setting_data['ide']

        print(file_path)
        with open(file_path, 'w'):
            pass

        os.system(f'{ide_cmd} {file_path}')

def submit_code(site_url, site_title, setting_data):
    # 코드를 제출하는 함수
    for i, url in enumerate(site_url):
        number, name = get_question_information(url, site_title[i])

        # 설정된 파일 이름 생성 
        file_name = create_name(number, name, setting_data)

        file_path = setting_data['path'] + file_name + setting_data['programing language']
        with open(file_path, 'r') as f:
            code = f.read()

        clipboard.copy(code)

        print(setting_data['submit url'] + number)
        webbrowser.open(setting_data['submit url'] + number)

        time.sleep(2)

        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('ctrl', 'enter')

def git_code(site_url, site_title, setting_data):
    # 깃허브 자동화 코드
    for i, url in enumerate(site_url):

        number, name = get_question_information(url, site_title[i])

        for j in setting_data['git automation']:
            if j == 'add':
                # git add
                git_path = create_file_path(url, site_title[i], setting_data)
                cmd = os.popen(f'git add {git_path}').read()
                print(cmd)

            elif j == 'commit':
                # git commit
                git_message = create_name(number, name, setting_data)
                cmd = os.popen(f'git commit -m {git_message}').read()
                print(cmd)

            elif j == 'push':
                # git push
                cmd = os.popen('git push').read()
                print(cmd)

            else:
                print(f"Error: {j} is not git command")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new", help="Create a new file.", action="store_true")
    parser.add_argument("-s", "--submit", help="Submit a file.", action="store_true")
    parser.add_argument("-g", "--git", help="Add, commit, and push files.", action="store_true")
    args = parser.parse_args()

    setting_data = load_settings()

    if args.new:
        browser_title = get_browser_title(setting_data)
        if browser_title:
            site_url, site_title = get_browser_url(browser_title, setting_data)
            if site_url:
                create_file(site_url, site_title, setting_data)
            else:
                print("Error: Not the specified page.")
        else:
            print("Error: Browser is not open.")

    if args.submit:
        browser_title = get_browser_title(setting_data)
        if browser_title:
            site_url, site_title = get_browser_url(browser_title, setting_data)
            if site_url:
                submit_code(site_url, site_title, setting_data)
            else:
                print("Error: Not the specified page.")
        else:
            print("Error: Browser is not open.")

    if args.git:
        browser_title = get_browser_title(setting_data)
        if browser_title:
            site_url, site_title = get_browser_url(browser_title, setting_data)
            if site_url:
                git_code(site_url, site_title, setting_data)
            else:
                print("Error: Not the specified page.")
        else:
            print("Error: Browser is not open.")
