import json
import time
import requests
from utility import (get_type_1017, decrypt, get_cb, get_random_id,
                     get_data, get_ssxmod_itna, get_hm_account,
                     get_gdxidpyhxde, get_necaptcha, get_snaker_id,
                     encode_uri_component)


class ValidateError(Exception):
    pass

class RequestError(Exception):
    pass

class Ctbpsp:
    def __init__(self):
        self.url = "https://ctbpsp.com/#/"
        self.selectIndex = 0
        self.cityList = ['', '安徽', '北京', '兵团', '重庆', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南',
                         '黑龙江', '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古', '宁夏', '青海', '山东',
                         '山西', '陕西', '上海', '四川', '天津', '西藏', '新疆', '云南', '浙江']
        self.industries = ['', "能源电力", "公路", "房屋建筑", "化学工业", "石油石化", "铁路", "园林绿化", "生物医药",
                           "水利水电", "水运", "港口航道", "纺织轻工", "矿产冶金", "民航", "生态环保", "地球科学",
                           "信息电子", "市政",
                           "广电通信", "科教文卫", "商业服务", "农林牧渔", "保险金融", "机械设备", "航空航天", "其他"]
        self._hm_headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://ctbpsp.com/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self._session = requests.session()
        self._session.get('https://ctbpsp.com/')

    def _get_config(self):
        call_id = "__JSONP_" + get_random_id() + "_0"
        _url = "https://c.dun.163.com/api/v2/getconf"
        _params = {
            "referer": "https://ctbpsp.com/#/",
            "zoneId": "",
            "id": "c5ecce1ce90c4837bcf6130104877673",
            "ipv6": "false",
            "runEnv": "10",
            "iv": "5",
            "loadVersion": "2.5.3",
            "callback": call_id
        }
        _response = requests.get(_url, headers=self._hm_headers, params=_params)
        _result = _response.text.replace(call_id, "")[1:-2]
        return json.loads(_result)

    def _get_v3_token(self, _dt, _fp):
        call_id = "__JSONP_" + get_random_id() + "_0"
        _url = "https://c.dun.163.com/api/v3/get"
        params = {
            "referer": "https://ctbpsp.com/#/",
            "zoneId": "CN31",
            "dt": _dt,
            "id": "c5ecce1ce90c4837bcf6130104877673",  # 固定 id
            "fp": _fp,
            "https": "true",
            "type": "",
            "width": "",
            "sizeType": "undefined",
            "version": "2.28.5",
            "dpr": "1",
            "dev": "1",
            "cb": get_cb(),
            "ipv6": "false",
            "runEnv": "10",
            "group": "",
            "scene": "",
            "sdkVersion": "",
            "loadVersion": "2.5.3",
            "iv": "4",
            "user": "",
            "irToken": "fEMMd8+3MatAMlBQAQfSngqL7LxBMACE",
            "smsVersion": "v3",
            "callback": call_id
        }
        _response = requests.get(_url, headers=self._hm_headers, params=params)
        _result = _response.text.replace(call_id, "")[1:-2]
        return json.loads(_result)

    def _get_v3_validate(self, _dt, _token, _t):
        call_id = "__JSONP_" + get_random_id() + "_1"
        _url = "https://c.dun.163.com/api/v3/check"
        _params = {
            "referer": "https://ctbpsp.com/#/",
            "zoneId": "CN31",
            "dt": _dt,
            "id": "c5ecce1ce90c4837bcf6130104877673",
            "version": "2.28.5",
            "cb": get_cb(),
            "user": "",
            "extraData": "",
            "bf": "0",
            "runEnv": "10",
            "sdkVersion": "undefined",
            "loadVersion": "2.5.3",
            "iv": "4",
            "token": _token,
            "type": "5",
            "width": "240",
            "data": get_data(_token, _t),
            "callback": call_id
        }
        _response = requests.get(_url, headers=self._hm_headers, params=_params)
        _result = _response.text.replace(call_id, "")[1:-2]
        return json.loads(_result)

    def _get_recommand_when_first_page(self, _page, _province, _industry, _validate, gdxidpyhxde):
        _url = f"https://ctbpsp.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/{_page}?province={encode_uri_component(_province)}&industry={encode_uri_component(_industry)}"
        type1017 = get_type_1017(_url)
        _url = _url + '&type__1017=' + type1017
        timestamp = str(int(time.time()))
        ssxmod = get_ssxmod_itna()
        cookies = {
            'gdxidpyhxdE': gdxidpyhxde,
            '__snaker__id': get_snaker_id(),
            'Hm_lvt_b966fe201514832da03dcf6cbf25b8a2': timestamp,
            'Hm_lpvt_b966fe201514832da03dcf6cbf25b8a2': timestamp,
            'HMACCOUNT': get_hm_account(),
            'ssxmod_itna': ssxmod[0],
            'ssxmod_itna2': ssxmod[1]
        }
        necaptcha = get_necaptcha(_validate, gdxidpyhxde)
        _headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Necaptcha-Validate": necaptcha,
            "Pragma": "no-cache",
            "Referer": "https://ctbpsp.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self._session.cookies.update(cookies)
        response = self._session.get(_url, headers=_headers)
        return json.loads(decrypt(response.text))

    def _get_qazx_config(self):
        _t = "VaptchaJsonp" + str(int(time.time() * 1000))
        _url = "https://qazx.vaptcha.net/config"
        params = {
            "vi": "65e97be7d3784602950e7d58",
            "t": "invisible",
            "s": "0",
            "z": "8",
            "v": "3",
            "u": "",
            "callback": _t
        }
        response = requests.get(_url, headers=self._hm_headers, params=params)
        return json.loads(response.text.replace(_t, '')[1:-2])

    def _get_recommand_in_other(self, _page, _province, _industry, v_token):
        _url = f"https://ctbpsp.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/{_page}?province={encode_uri_component(_province)}&industry={encode_uri_component(_industry)}"
        type1017 = get_type_1017(_url)
        _url = _url + '&type__1017=' + type1017
        _headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://ctbpsp.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "V-Token": v_token # todo
        }

    def get_search_result_list(self, _page, _province, _industry):
        print(f'第 {_page} 页 | 地区：{_province} | 行业：{_industry}')
        time.sleep(0.4)
        start_time = int(time.time() * 1000)
        result = self._get_config()
        dt = result['data']['dt']
        fp = get_gdxidpyhxde()
        result = self._get_v3_token(dt, fp)
        token = result['data']['token']
        result = self._get_v3_validate(dt, token, start_time)
        validate = result['data']['validate']
        if validate:
            print('获取 validate 成功!')
            time.sleep(0.3)
            result = self._get_recommand_when_first_page(_page, _province, _industry, validate, fp)
            if not result['success']:
                raise RequestError(f"请求数据失败: {result}")
        else:
            raise ValidateError("获取 validate 失败！重新尝试获取...")

    def run(self):
        try:
            self.get_search_result_list(1, '', '')
        except requests.ConnectionError as e:
            print(f"连接失败: {str(e)}")
        except ValidateError as e:
            print(e)
        except RequestError as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f'未知异常: {e}')


if __name__ == '__main__':
    Ctbpsp().run()
