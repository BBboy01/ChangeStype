import requests
import json
import time
import random
import gevent
from hashlib import md5


class Step:
    def __init__(self, users):
        self.user_info = users
        self.login_url = "https://sports.lifesense.com/sessions_service/login?" \
                         "platform=android&systemType=2&version=4.6.7"
        self.step_url = "https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?" \
                        "version=4.5&systemType=2"

    def get_id_token(self, phone, pwd):
        header_login = {'Content-Type': 'application/json; charset=utf-8',
                        'Accept-Encoding': 'gzip',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; MI 8 MIUI/V12.0.1.0.QEACNXM)'
                        }
        data_org_login = {"appType": 6, "clientId": "88888", "loginName": phone,
                          "password": md5(pwd.encode(encoding="utf-8")).hexdigest(), "roleType": 0}
        data_login = json.dumps(data_org_login)
        resp_data = json.loads(requests.post(url=self.login_url, data=data_login, headers=header_login).text)
        uid = resp_data['data']['userId']
        token = resp_data['data']['accessToken']

        return uid, token, phone

    def set_step(self, uid, token, phone, step):
        header_step = {'Cookie': 'accessToken=' + token,
                       'Content-Type': 'application/json; charset=utf-8'
                       }
        data_org_step = {"list":
                             [{"DataSource": 2,
                               "active": 1,
                               "calories": str(int(step // 20)),
                               "dataSource": 2,
                               "deviceId": "M_NULL",
                               "distance": int(step / 3),
                               "exerciseTime": 0,
                               "isUpload": 0,
                               "measurementTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                               "priority": 0,
                               "step": step,
                               "type": 2,
                               "updated": float(str(time.time()).split(".")[0]) + float(str(time.time()).split(".")[1][:3]),
                               "userId": uid}]
                         }
        data_step = json.dumps(data_org_step)
        result = json.loads(requests.post(url=self.step_url, data=data_step, headers=header_step).text)
        data = list(set(result['data']['pedometerRecordHourlyList'][0]['step'].split(",")))

        # print(step, int(max(data)), data)
        for i in range(len(data)):
            data[i] = int(data[i])

        if step > max(data):
            print(phone, ":", step)
        else:
            print(phone, ":", max(data))

    def run(self):
        for phone, pwd in self.user_info.items():
            jobs = [gevent.spawn(self.set_step, *(self.get_id_token(phone, pwd)), random.randint(7000, 15000))]
            gevent.joinall(jobs)


if __name__ == '__main__':
    user_info = {"phone_number": "password",
                 }  # add your target dict here
    zqy = Step(user_info)
    zqy.run()
