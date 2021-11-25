import base64
import json
import re
import time
import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class ClockIn:
    __cookie = ""
    __username = ""
    __password = ""
    __login_url = "https://app.bupt.edu.cn/uc/wap/login/check"
    __upload_url = "https://app.bupt.edu.cn/ncov/wap/default/save"

    def __init__(self, _username, _password):
        self.__username = _username
        self.__password = _password

    def __get_cookie(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 "
                          "Safari/537.36"
        }
        data = {
            "username": self.__username,
            "password": self.__password
        }
        res = requests.post(url=self.__login_url, headers=headers, data=data)
        for key, value in res.cookies.items():
            self.__cookie += key + "=" + value + "; "
        return self.__cookie[:-2]

    def __get_html(self):
        self.__get_cookie()
        url = "https://app.bupt.edu.cn/ncov/wap/default/index?from=history"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 "
                          "Safari/537.36",
            "cookie": self.__cookie
        }
        res = requests.get(url=url, headers=headers)
        return res.text

    def __get_old_info(self):
        res = BeautifulSoup(self.__get_html(), "html.parser")
        script = list(res.select("script[type='text/javascript']"))[1]
        pattern = re.compile(r"oldInfo: {.*?},$", re.MULTILINE | re.DOTALL)
        s = json.loads(re.findall(pattern, str(script))[0][9:-1])
        s["created"] = int(time.time())
        s["date"] = time.strftime("%Y%m%d")
        return s

    def save(self):
        jsonobj = self.__get_old_info()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 "
                          "Safari/537.36",
            "cookie": self.__cookie
        }
        res = requests.post(url=self.__upload_url, headers=headers, data=jsonobj)
        return res.text


def upload(username, password):
    clock_in = ClockIn(username, password)
    msg = clock_in.save()
    return msg


def push_msg(msg: str, js: json):
    push_url = "http://wxpusher.zjiecode.com/api/send/message"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "appToken": js["appToken"],
        "content": msg,
        "contentType": 1,
        "uids": [js["uid"]],
    }
    if js["appToken"] == "" or js["uid"] == "":
        return
    res = requests.post(url=push_url, headers=headers, json=data)
    return res


def main():
    with open(os.path.dirname(__file__) + "/config.json", "r") as f:
        data = json.load(f)
    count = 0
    for item in data:
        for i in range(3):
            time.sleep(i * 5)
            msg = upload(data[item]["username"], data[item]["password"])
            if json.loads(msg)["m"] == "今天已经填报了" or json.loads(msg)["m"] == "操作成功":
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + json.loads(msg)["m"])
                push_msg(time.strftime("%Y-%m-%d %H:%M:%S") + " " + json.loads(msg)["m"], data[item])
                count += 1
                if count == len(data):
                    return
                else:
                    break
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + json.loads(msg)["m"])
                push_msg(time.strftime("%Y-%m-%d %H:%M:%S") + " " + json.loads(msg)["m"], data[item])


if __name__ == '__main__':
    main()
