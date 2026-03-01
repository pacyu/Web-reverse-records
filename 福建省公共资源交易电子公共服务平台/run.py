import json
import time
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt(cipher_text):
    key = b'EB444973714E4A40876CE66BE45D5930'
    iv = b'B5A8904209931867'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(base64.b64decode(cipher_text)), AES.block_size)
    return decrypted_data.decode('utf-8')

def get_sign(params):
    sorted_keys = sorted(params, key=str.upper)
    _n = 'B3978D054A72A7002063637CCDF6B2E5' + ''.join([k+str(params[k]) for k in sorted_keys if params[k]])
    return hashlib.md5(_n.encode()).hexdigest()


def get_page_list():
    """
    主页：https://ggzyfw.fj.gov.cn/business/list/
    """
    url = "https://ggzyfw.fj.gov.cn/FwPortalApi/Trade/TradeInfo"
    _t = int(time.time() * 1000)
    data = {
    'pageNo': 1,
    'pageSize': 20,
    'total': 3456,
    'AREACODE': '',
    'M_PROJECT_TYPE': '',
    'KIND': 'GCJS',
    'GGTYPE': '1',
    'PROTYPE': '',
    'timeType': '6',
    'BeginTime': '2025-06-27 00:00:00',
    'EndTime': '2025-12-27 23:59:59',
    'createTime': '',
    'ts': _t,
}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "portal-sign": get_sign(data),
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)
    return decrypt(response.json()['Data'])

print(get_page_list())