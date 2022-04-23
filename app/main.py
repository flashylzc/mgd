import hashlib
import json
import requests
import yaml
import os
""" 一些全局变量配置文件"""
LoginUrl = 'https://api.moguding.net:9000/session/user/v1/login'
saveUrl = 'https://api.moguding.net:9000/attendence/clock/v2/save'
healthyUrl = "https://api.moguding.net:9000/practice/hlj/health/reports/v1/save"
ReportUrl = "https://api.moguding.net:9000/practice/paper/v2/save"
# 加密密钥
salt = "3478cbbc33f84bd00d75d7dfa69e0daa"
headers = {
    'Accept-Language': "zh-CN,zh;q=0.8",
    'roleKey': 'student',
    'Host': 'api.moguding.net:9000',
    "Content-Type": "application/json; charset=UTF-8",
    "Cache-Control": "no-cache",
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-cn; RMX2072 Build/RKQ1.200710.002) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
}


def load(path):
    """ 从config.yaml文件读取数据 """
    yamlPath = path
    file = open(yamlPath, encoding='utf=8')
    data = file.read()
    file.close()
    data = yaml.load(data, Loader=yaml.FullLoader)
    # print(data)
    """ 声明一些全局变量,并通过配置文件赋值 """
    # 签到状态:END 或者START
    global state
    state = data['Clock']['state']
    # sign参数
    global sign
    # 国家
    global country
    country = data['Clock']['country']
    # 详细地址
    global address
    address = data['Clock']['address']
    # 省份
    global province
    province = data['Clock']['province']
    # 地区
    global city
    city = data['Clock']['city']
    # 纬度
    global latitude
    latitude = data['Clock']['latitude']
    # 经度
    global longitude
    longitude = data['Clock']['longitude']
    # 密码
    global password
    # password = data['Login']['password']
    password = input()
    # 账号
    global phone
    # phone = data['Login']['phone']
    phone = input()
    # 健康日报
    global healthyData
    # healthyData = data['healthyData']


def login():
    """ 登录函数,返回Response对象 """
    print("正在登录......")
    global token, userId
    data = {
        "password": password,
        "phone": phone,
        "loginType": "android",
        "uuid": ""
    }
    try:
        requests.packages.urllib3.disable_warnings()  # 不提示warnings
        resp = requests.post(LoginUrl, headers=headers,
                             data=json.dumps(data), verify=False)
        inFo = resp.json()
        if inFo['code'] == 200:
            global studentName
            studentName = inFo['data']['nikeName']
            token = inFo['data']['token']
            userId = inFo['data']['userId']
            print("登录成功------"+studentName)
            print("token------"+token)
            print("userId------"+userId)
        else:
            print("登陆失败------"+inFo['msg'])
    finally:
        pass
    return resp


def Clock(state):
    """ 签到函数 """
    data = {
        'country': country,
        'address': address,
        'province': province,
        'city': city,
        'latitude': latitude,
        'planId': planId,
        'type': state,
        'device': 'Android',
        'longitude': longitude
    }
    # sign= device + type + planID + userId + Address + salt
    headers["sign"] = GenerateSign(
        data["device"]+data["type"]+planId+userId+data["address"]+salt)
    if state == "START":
        print("正在执行上班签到......")
    else:
        print("正在执行下班签到......")
    resp = requests.post(url=saveUrl, headers=headers, data=json.dumps(data))
    inFo = resp.json()
    if inFo['code'] == 200:
        print("签到成功------"+inFo['data']['createTime'])
    else:
        print("签到失败------"+inFo['msg'])

    return resp


def GenerateSign(x):
    """ 生成签名sign """
    a = x.encode('utf-8')
    a = hashlib.md5(a).hexdigest()
    # print(a)
    return a


def healthyReport():
    """ 健康日报上报 """
    htRsp = requests.post(url=healthyUrl, headers=headers,
                          data=json.dumps(healthyData))
    htInfo = htRsp.json()
    print(htInfo)
    return htInfo


def getPlanId():
    """ 获取参数planId """
    planUrl = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
    print('获取PlanId......')
    global planId
    headers["Authorization"] = token
    headers["sign"] = GenerateSign(userId+"student"+salt)
    data = {}
    rsp = requests.post(url=planUrl, data=json.dumps(data), headers=headers)
    planId = rsp.json()['data'][0]['planId']
    print("planId\t"+planId)


def main(path):
        # 加载数据
        load(path=path)
        # 登录
        login()
        # 获取planId
        getPlanId()
        # 上班签到
        Clock(state)
        # 健康日报

""" 入口函数 """
if __name__ == "__main__":
#     main('XYconfig.yaml')
    main('config.yaml')
#     main('LJconfig.yaml')
