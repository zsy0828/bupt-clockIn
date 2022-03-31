import json
import os
import time

import schedule

import req_model


def main(js: json):
    for i in range(3):
        time.sleep(i * 5)
        if data[item]["username"] != "" and data[item]["password"] != "":
            msg = req_model.upload(js)
            if msg == "":
                print(time.strftime("%H:%M") + " " + "打卡失败！！！！")
                req_model.push_msg(time.strftime("%H:%M") + " " + "打卡失败！！！！", data[item])
            elif json.loads(msg)["m"] == "今天已经填报了" or json.loads(msg)["m"] == "操作成功":
                print(time.strftime("%H:%M") + " " + json.loads(msg)["m"])
                req_model.push_msg(time.strftime("%H:%M") + " " + json.loads(msg)["m"], js)
                return
            else:
                print(time.strftime("%H:%M") + " " + json.loads(msg)["m"])
                req_model.push_msg(time.strftime("%H:%M") + " " + json.loads(msg)["m"], js)


if __name__ == '__main__':
    with open(os.path.dirname(__file__) + "/config.json", "r") as f:
        data = json.load(f)
    for item in data:
        schedule.every().day.at(data[item]["time"]).do(main, data[item])
    while 1:
        time.sleep(1)
        schedule.run_pending()
