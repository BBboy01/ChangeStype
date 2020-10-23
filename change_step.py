import requests
import json
import time
from hashlib import md5


phone = "15829952062"
pwd = "244466666"

step = 13333

login_url = "https://sports.lifesense.com/sessions_service/login?platform=android&systemType=2&version=4.6.7"
step_url = "https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?version=4.5&systemType=2"
header_login = {'Content-Type': 'application/json; charset=utf-8',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; MI 8 MIUI/V12.0.1.0.QEACNXM)'
            }
data_org_login = {"appType" : 6, "clientId" : "88888", "loginName" : phone, "password" : md5(pwd.encode(encoding="utf-8")).hexdigest(), "roleType" : 0}
data_login = json.dumps(data_org_login)
resp_data = json.loads(requests.post(url=login_url, data=data_login, headers=header_login).text)

uid = resp_data['data']['userId']
tocken = resp_data['data']['accessToken']

time_stamp = str(time.time()).split(".")
sec = float(time_stamp[0]) + float(time_stamp[1][:3])
header_step = {'Cookie': 'accessToken=' + tocken,
        'Content-Type': 'application/json; charset=utf-8'
        }
data_org_step = {"list" :
        [{"DataSource" : 2,
        "active" : 1,
        "calories":  str(int(step // 20)),
        "dataSource" : 2,
        "deviceId" : "M_NULL",
        "distance":  int(step / 3),
        "exerciseTime" : 0,
        "isUpload" : 0,
        "measurementTime" : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        "priority" : 0,
        "step" : step,
        "type" : 2,
        "updated" : sec,
        "userId" : uid}]
        }
data_step = json.dumps(data_org_step)

result = json.loads(requests.post(url=step_url, data=data_step, headers=header_step).text)
print(result['data']['pedometerRecordHourlyList'][0]['step'])
