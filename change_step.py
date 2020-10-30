import requests
import json
import time
import random
# import gevent
from hashlib import md5
# from gevent import monkey


class Step:
    def __init__(self, users):
        self.user_info = users
        self.login_url = "https://sports.lifesense.com/sessions_service/login?" \
                         "platform=android&systemType=2&version=4.6.7"
        self.step_url = "https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?" \
                        "version=4.5&systemType=2"
        self.user_agent = "Dalvik/2.1.0 (Linux; U; Android 9; SM-G9500 Build/PPR1.180610.011)"
        self.band_ids = ["http://we.qq.com/d/AQC7PnaOelOaCg9Ux8c9Ew95yumTVfMcFuGCHMY-",
                         "http://we.qq.com/d/AQC7PnaOi9BLVrfJIiVTU8ENIbv_9Lmlqia1ToGc",
                         "http://we.qq.com/d/AQC7PnaOXQhy3VvzFeP5bZMKmAQrGE6NJWdK3Xnk",
                         "http://we.qq.com/d/AQC7PnaOaEXBdhkdXQvTRE1CO1fIqBuitbSSGt2r",
                         "http://we.qq.com/d/AQC7PnaOdI9h0tfCr0KRlb78ISAE9qcaZ3btHrJE",
                         "http://we.qq.com/d/AQC7PnaOsThRYksmQcvpa0klKFrupqaqKyEPm8nj",
                         "http://we.qq.com/d/AQC7PnaOk8V-FV7R4ix61GToC5fh5I151hvlsNf6",
                        ]
        self.bind_msg = ''


    def get_id_token(self, phone, pwd):
        header_login = {'Content-Type': 'application/json; charset=utf-8',
                        'Accept-Encoding': 'gzip',
                        'User-Agent': self.user_agent
                        }
        data_org_login = {"appType": 6, "clientId": md5(phone.encode(encoding="utf-8")).hexdigest(), "loginName": phone,
                          "password": md5(pwd.encode(encoding="utf-8")).hexdigest(), "roleType": 0}
        data_login = json.dumps(data_org_login)
        resp_data = json.loads(requests.post(url=self.login_url, data=data_login, headers=header_login).text)
        uid = resp_data['data']['userId']
        token = resp_data['data']['accessToken']

        return uid, token, phone


    def bind_device(self, uid, token):
        bind_url = "https://sports.lifesense.com/device_service/device_user/bind"
        band_id = random.choice(self.band_ids)
        bind_org_data = {
                        "qrcode": band_id,
                        "userId": int(uid)
                        }
        bind_data = json.dumps(bind_org_data)
        bind_header = {
                    "Content-Type": "application/json; charset=utf-8",
                    "Cookie": "accessToken=" + token,
                    "User-Agent": self.user_agent
                    }
        bind_result = requests.post(url=bind_url, data=bind_data, headers=bind_header)
        self.bind_msg = json.loads(bind_result.text)['msg']
        time.sleep(5)


    def set_step(self, uid, token, phone, step):
        self.bind_device(uid, token)
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
        time.sleep(3)
        result = json.loads(requests.post(url=self.step_url, data=data_step, headers=header_step).text)
        data = list(set(result['data']['pedometerRecordHourlyList'][0]['step'].split(",")))

        for i in range(len(data)):
            data[i] = int(data[i])

        if step > max(data):
            print("手机号:", phone, " 当前步数:", step, " 绑定情况:", self.bind_msg)
        else:
            print("手机号:", phone, " 当前步数:", max(data), "绑定情况:", self.bind_msg)


    def run(self):
        for phone, pwd in self.user_info.items():
            self.set_step(*(self.get_id_token(phone, pwd)), random.randint(7000, 15000))
            time.sleep(2)
            # jobs = [gevent.spawn(self.set_step, *(self.get_id_token(phone, pwd)), random.randint(7000, 15000))]
            # gevent.joinall(jobs)


if __name__ == '__main__':
    # monkey.patch_all()
    user_info = {"13389186408": "123456789",
                 "18706731417": "123456789",
                 "17792469938": "123456789",
                 "18329478998": "123456789",
                 "13098043070": "mp200529.0",
                 "18591880102": "123456789",
                 "15829952062": "244466666",
                 "18740431190": "zyl19980608",
                 }
    zqy = Step(user_info)
    zqy.run()
