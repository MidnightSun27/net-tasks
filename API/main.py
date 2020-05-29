#!/usr/bin/env python3
# -*- coding: utf-8 -*-а

import webbrowser
from urllib import request as req
import json
import sys

APP_ID = "7489478"


def authorization():
    try:
        with open("token.txt", "r") as file:
            token = file.read()
    except FileNotFoundError:
        auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                    "&scope=wall,friends&redirect_"
                    "uri=http://oauth.vk.com/blank.html"
                    "&display=page&response_type=token".format(app_id=APP_ID))
        webbrowser.open_new_tab(auth_url)
        token = input("Paste token here: ")
        with open("token.txt", "w") as file:
            file.write(token)
    return token


def get_help():
    print("Этот скрипт позволяет вывести список друзей для указанного профиля в Вконтакте.")
    print("Инструкции:")
    print("Введите id-адрес или ссылку на страницу желаемого профиля сразу после \"python3 main.py\"")
    print("Пример запуска:")
    print("python3 main.py https://vk.com/solodushkin_si  | python3 main.py solodushkin_si")
    print("В открывшейся вкладке браузера появится авторизация пользователя.")
    print("Нажмите на \"Разрешить\" и далее в новой странице адресной строке будет URL "
          "\"https://oauth.vk.com/blank.html\".")
    print("А после # Вы увидите дополнительные параметры — access_token, expires_in и user_id.")
    print("Скопируйте последовательность букв и цифр, после \"access_token=\" и перед \"expires_in\"и вставьте в "
          "консоль после получения просьбы \"Paste token here:\".")
    print("Для запуска инструкции снова:")
    print("Запустить скрипт без аргумента:  python3 main.py")
    print("python3 main.py --help | python3 main.py -h")

    print("Онуфриенко Т.Р., МЕН-282201")


def main():
    if len(sys.argv) == 1:
        get_help()
        return
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        get_help()
        return
    profile_id = sys.argv[1].strip()
    token = authorization()
    base = "https://vk.com/"
    if base in profile_id:
        profile_id = profile_id[len(base):]
    r = req.urlopen(
        "https://api.vk.com/method/users.get?user_ids={}&v=5.95&access_token={}".format(profile_id, token))
    response = json.loads(r.read())
    if "error" in response:
        print("Error {}: {}".format(response["error"]["error_code"],
                                    response["error"]["error_msg"]))
        return
    response = response["response"][0]
    user_info = response["first_name"] + " " + response["last_name"]
    profile_id = response["id"]
    f = req.urlopen(
        "https://api.vk.com/method/friends.get?user_id={}&order=name&fields=online&v=5.95&access_token={}".format(
            profile_id, token))
    another_response = json.loads(f.read())
    if "error" in another_response:
        print("Error {}: {}".format(response["error"]["error_code"],
                                    response["error"]["error_msg"]))
        return
    another_response = another_response["response"]
    count = str(another_response["count"])
    friends = another_response["items"]
    print(user_info)
    print("Amount of friends: " + count)
    online_now = 0
    for friend in friends:
        online = "offline"
        name = friend["first_name"] + " " + friend["last_name"]
        if friend["online"] == 1:
            online = "online"
            online_now += 1
        print("{} is {}".format(name, online))
    print("___________________________________")
    print("Online now: {}".format(online_now))



if __name__ == '__main__':
    main()
