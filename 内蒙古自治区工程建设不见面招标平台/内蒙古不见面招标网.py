import time
import uuid
import requests
from gmssl.sm3 import sm3_hash
from urllib.parse import quote

def encode_str(_s):
    return (quote(_s).replace("'", '%27')
            .replace("!", '%21')
            .replace("~", '%7E')
            .replace("(", '%28')
            .replace(")", '%29')
            .replace("/", '%2F'))

def sm3encrypt(text):
    return sm3_hash(list(text.encode('utf-8'))).upper()

def get_sign(_data, _url):
    uid = str(uuid.uuid1())
    req_time = str(int(time.time() * 1000))
    param_sign = sm3encrypt(uid + ';' + req_time + ';' + encode_str(_url))
    dto_sign = sm3encrypt(uid + ';' + req_time + ';' + encode_str(data['commonDto']) + ';' + encode_str(data['cmdParams']))
    _data.update({
        'replaynoticeid': uid,
        'reqtime': req_time,
        'paramsign': param_sign,
        'dtosign': dto_sign
    })

def user_token(n, a, title):
    return 'userToken=' + n + ',reqTime=' + a + ',deviceId=b1f0e63a791657f022aedd30a6697b02,' + quote(title)


session = requests.Session()
login_url = 'https://219.148.175.179:9443/BidOpening/rest/loginaction/login?isCommondto=true'
data = {
    'commonDto': "[{\"id\":\"_common_hidden_viewdata\",\"type\":\"hidden\",\"value\":\"{\\\"pageurl\\\":\\\"43c8ac72ab8d9e9eee31536960a05aec5cbba4e5b790995b8dfc0bec987ea6d2\\\"}\"}]",
    'cmdParams': "{\"loginType\":\"3\",\"userType\":\"Guest\",\"userName\":\"043d94e5602e965909d37b3f8474229287f7e0cde7d5fce22270e2d4722637e404b1fed611ae70e0d0f3e41636f7180dde1dbe244b7f101d82090121eead169660cd9195a5eae82509c8adc4982acf724745780ab5fd700f47249a06eae03fb75dac15ac2c\",\"password\":null,\"CAKey\":null,\"platformCode\":\"ZZQBJM\",\"code\":\"\",\"extvals\":{\"ClientTime\":%s},\"passWord\":\"123456\"}" % str(int(time.time() * 1000))
}
get_sign(data, 'isCommondto=true')
# print(data['dtosign'])
# print(data['paramsign'])
# assert False
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Token': user_token('', str(int(time.time() * 1000)), '登录页'),
    'X-Requested-With': 'XMLHttpRequest',
}
session.post(login_url, headers=headers, data=data)

page_load_url = 'https://219.148.175.179:9443/BidOpening/rest/homepageaction/page_load?isCommondto=true'
data = {
    "commonDto": "[{\"id\":\"areaType\",\"type\":\"combobox\",\"action\":\"getAreaCodes\",\"name\":\"areaType\",\"pinyinField\":\"tag\",\"columns\":[],\"textField\":\"text\",\"valueField\":\"id\",\"value\":\"\",\"text\":\"\"},{\"id\":\"_common_hidden_viewdata\",\"type\":\"hidden\",\"value\":\"\"}]",
    "cmdParams": "{\"pageUrl\":\"https://219.148.175.179:9443/BidOpening/bidhall/default/home\"}",
}
get_sign(data, 'isCommondto=true')
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Token': user_token('', str(int(time.time() * 1000)), '不见面开标大厅列表页'),
    'X-Requested-With': 'XMLHttpRequest',
}
r = session.post(page_load_url, headers=headers, data=data)
for control in r.json()['controls']:
    if control['id'] == '_common_hidden_viewdata':
        value = control['value']
        print(value)
        break
# ZZQBJM&