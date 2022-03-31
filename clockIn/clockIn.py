import json
import os
import time

import req_model


def main():
    with open(os.path.dirname(__file__) + "/config.json", "r") as f:
        data = json.load(f)
    count = 0
    for item in data:
        for i in range(3):
            time.sleep(i * 5)
            if data[item]["username"] != "" and data[item]["password"] != "":
                msg = req_model.upload(data[item]["username"], data[item]["password"])
                if msg == "":
                    print(time.strftime("%H:%M") + " " + "打卡失败！！！！")
                    req_model.push_msg(time.strftime("%H:%M") + " " + "打卡失败！！！！", data[item])
                elif json.loads(msg)["m"] == "今天已经填报了" or json.loads(msg)["m"] == "操作成功":
                    print(time.strftime("%H:%M") + " " + json.loads(msg)["m"])
                    req_model.push_msg(time.strftime("%H:%M") + " " + json.loads(msg)["m"], data[item])
                    count += 1
                    if count == len(data):
                        return
                    else:
                        break
                else:
                    print(time.strftime("%H:%M") + " " + json.loads(msg)["m"])
                    req_model.push_msg(time.strftime("%H:%M") + " " + json.loads(msg)["m"], data[item])


if __name__ == '__main__':
    main()
