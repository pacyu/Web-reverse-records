import re
import json
import time
import zlib
import base64
import ctypes
import random
import requests
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from urllib.parse import quote
from datetime import datetime, timezone

XS = [
    "760253670a19b2b0a88e2",
    "websdk-2.3.15d",
    1765954466543,
    154,
    "1|15",
    "zh-CN",
    -480,
    "16705151|12791",
    "1920|1080|1795|925|8|41|1920|1080|1811|1020|0|0",
    3,
    "Win32",
    12,
    "ANGLE (Intel, Intel(R) UHD Graphics 730 (0x00004682) Direct3D11 vs_5_0 ps_5_0, D3D11)|Google Inc. (Intel)",
    "24|24",
    0,
    28,
    "5|1318940364",
    3849571061,
    97803781,
    1,
    0,
    0,
    0
]
XL = [
    416,
    "Google Inc.",
    8,
    "12|8|3|2|0",
    3726056879
]
XD = [
    599647252,
    0,
    29
]


def encode_uri_component(_text):
    return quote(str(_text), safe="~()*!.'")

def calculate_hash(p0):
    p2 = 0
    # 遍历字符串
    for char in p0:
        p2 = (p2 << 7) - p2 + 398 + ord(char)
        # 强制转换为 32 位有符号整数 (模拟 JS 的位运算行为)
        p2 = ctypes.c_int32(p2).value
    return p2

def compress(p3, p4, p5_map):
    if not p3: return ""

    p9 = {}  # 字典：字符串 -> 索引
    pX = {}  # 标记：是否为新字符
    pp = ""  # 前缀
    pm = 2  # 初始步长
    pO = 3  # 初始索引偏移
    pb = 2  # 初始位宽
    pF = []  # 结果集
    pq = 0  # 位缓冲区
    pW = 0  # 缓冲区指针

    for pc in p3:
        if pc not in p9:
            p9[pc] = pO
            pO += 1
            pX[pc] = True

        pY = pp + pc
        if pY in p9:
            pp = pY
        else:
            # 输出前缀 pp 的编码
            if pp in pX:
                char_code = ord(pp[0])
                # 写入标记位 (LZW 变体中 0 代表 8位)
                for _ in range(pb):
                    pq <<= 1
                    if pW == p4 - 1:
                        pW = 0
                        pF.append(p5_map[pq])
                        pq = 0
                    else:
                        pW += 1

                # 写入 8 位字符
                for _ in range(8):
                    pq = (pq << 1) | (char_code & 1)
                    if pW == p4 - 1:
                        pW = 0
                        pF.append(p5_map[pq])
                        pq = 0
                    else:
                        pW += 1
                    char_code >>= 1

                pm -= 1
                if pm == 0:
                    pm = 2 ** pb
                    pb += 1
                del pX[pp]
            else:
                # 写入已有字典索引
                val = p9[pp]
                for _ in range(pb):
                    pq = (pq << 1) | (val & 1)
                    if pW == p4 - 1:
                        pW = 0
                        pF.append(p5_map[pq])
                        pq = 0
                    else:
                        pW += 1
                    val >>= 1

            pm -= 1
            if pm == 0:
                pm = 2 ** pb
                pb += 1

            p9[pY] = pO
            pO += 1
            pp = pc

    # 处理最后的 pp 节点
    if pp:
        if pp in pX:
            char_code = ord(pp[0])
            for _ in range(pb):
                pq <<= 1
                if pW == p4 - 1:
                    pW = 0
                    pF.append(p5_map[pq])
                    pq = 0
                else:
                    pW += 1
            for _ in range(8):
                pq = (pq << 1) | (char_code & 1)
                if pW == p4 - 1:
                    pW = 0
                    pF.append(p5_map[pq])
                    pq = 0
                else:
                    pW += 1
                char_code >>= 1
        else:
            val = p9[pp]
            for _ in range(pb):
                pq = (pq << 1) | (val & 1)
                if pW == p4 - 1:
                    pW = 0
                    pF.append(p5_map[pq])
                    pq = 0
                else:
                    pW += 1
                val >>= 1

    # 【关键修正点】：EOF 标记的处理
    # 该算法通常有一个隐藏的 EOF（通常是索引 2）
    eof_val = 2
    for _ in range(pb):
        pq = (pq << 1) | (eof_val & 1)
        if pW == p4 - 1:
            pW = 0
            pF.append(p5_map[pq])
            pq = 0
        else:
            pW += 1
        eof_val >>= 1

    # 最后补全缓冲区
    while True:
        pq <<= 1
        if pW == p4 - 1:
            pF.append(p5_map[pq])
            break
        pW += 1

    return "".join(pF)

def o(p3, p4):
    p5 = "DGi0YA7BemWnQjCl4+bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ"
    if p4:
        p5 = p5.replace('+', '_')
    p6 = compress(p3, 6, p5)
    return p6

def get_type_1017(p1):
    p3 = encode_uri_component(p1)
    p6 = str(calculate_hash(p3))
    p6 = p6 + '|' + '0|' + str(int(time.time() * 1000)) + '|1'
    # -1105898346|0|1765956470162|1
    # n4+hDKAKD5YvPQqGKG=D/tF4BK8fpio61iixYwID
    p7 = o(p6, None)
    return encode_uri_component(p7)

def decrypt(cipher_text):
    key = b'1qaz@wsx'
    des = DES.new(key, DES.MODE_ECB)
    decrypted_raw = des.decrypt(base64.b64decode(cipher_text))
    return unpad(decrypted_raw, 8, style='pkcs7').decode('utf-8')

def cz():
    p0 = {
        "F": [
            "911+734+131129",
            "-10+-14+32",
            "-8+-11+34",
            "-5+-7+37",
            "-7+-10+34",
            "-4+-8+34",
            "-3+-4+30",
            "-3+-4+32",
            "-2+-2+32",
            "-3+-4+32",
            "-1+-2+74",
            "-1+-2+756",
            "-667+-197+4250",
            "-20+27+31",
            "-24+19+35",
            "-15+20+38",
            "-16+12+32",
            "-19+15+32",
            "-1+4+111",
            "4+2+45",
            "14+2+35",
            "6+0+32",
            "14+1+32",
            "19+8+33",
            "20+5+32",
            "36+9+33",
            "52+2+31",
            "56+0+32",
            "103+-5+33",
            "107+1+34",
            "44+3+31",
            "-17+6+31",
            "1+1+127",
            "42+-5+32",
            "174+14+33",
            "174+65+31",
            "33+86+32",
            "-76+173+33",
            "-712+-257+2135",
            "-4+-2+32",
            "-5+-2+32",
            "-10+0+33",
            "-7+0+33",
            "-7+0+31",
            "-4+0+49",
            "-1+-3+94",
            "-2+1+32",
            "-4+8+38",
            "18+16+35",
            "13+149+1055",
            "-70+-77+33",
            "-50+-67+33",
            "-26+-38+31",
            "-7+-14+31",
            "-1+-6+95",
            "1+0+89",
            "33+0+33",
            "49+2+31",
            "51+7+32",
            "49+10+32",
            "47+14+32",
            "52+24+34",
            "37+24+30",
            "12+74+32",
            "5+154+33",
            "5+171+39",
            "5+131+32",
            "9+59+34",
            "4+11+47",
            "5+3+32",
            "6+3+31",
            "5+2+33",
            "13+5+32",
            "15+5+33",
            "6+47+38",
            "2+68+49",
            "6+89+31",
            "-69+53+403",
            "0+-5+37",
            "-2+-5+44",
            "0+-1011+195",
            "18+0+39",
            "51+-10+34",
            "82+-16+32",
            "121+-9+34",
            "103+6+35",
            "143+35+34",
            "76+21+33",
            "56+20+32",
            "23+11+32",
            "2+0+40",
            "0+2+34",
            "2+2+31",
            "1+0+71",
            "-5+8+31",
            "-23+21+32",
            "-52+38+32",
            "-82+57+33",
            "-72+60+32",
            "-52+61+32",
            "-567+-339+1192"
        ],
        "q": [
            "10+106+493+123795",
            "11+106+493+71",
            "10+926+755+7082",
            "11+864+666+1294",
            "10+101+564+4518",
            "11+106+568+75",
            "10+29+642+4464",
            "11+29+642+95",
            "10+374+1586+1316",
            "11+374+1586+68"
        ],
        "W": 5,
        "T": "P",
        "u": 21,
        "w": 123795,
        "D": [
            "0291"
        ],
        "K": 1
    }
    return p0

def xm(p0, p1, p2, p3):
    return p0 + '=' + p1 + ';expires=' + p2 + ';path=/;domain=' + p3

def get_ssxmod_itna():
    timestamp = int(time.time() * 1000)
    p1 = datetime.fromtimestamp((timestamp + 1800000) / 1000.0, tz=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    ci = "ctbpsp.com"
    p2 = cz()
    _ssxmod_itna = '1-' + o('^'.join([
        '^'.join(str(_) for _ in XS),
        '^'.join([p2['T'], str(len(p2['F'])), str(len(p2['q'])), str(len(p2['D']))]),
        '^'.join(str(_) for _ in XL),
        str(11), str(timestamp),
        '^'.join(str(_) for _ in XD)]), True)
    # ssxmod_itna = xm('ssxmod_itna', _ssxmod_itna, p1, ci)

    _ssxmod_itna2 = '1-' + o('^'.join(str(_) for _ in XS[:4]) + '^' + '^'.join([
        p2['T'], str(p2['u']), '|'.join(str(_) for _ in p2['F']), str(p2['w']),
        '|'.join(str(_) for _ in p2['q']), '|'.join(str(_) for _ in p2['D']), str(p2['K']),
        '0', '0', '11', str(timestamp), '0', '0', str(p2['W']), '4', '0']), True)
    # ssxmod_itna2 = xm('ssxmod_itna2', _ssxmod_itna2, p1, ci)
    return _ssxmod_itna, _ssxmod_itna2

def random_uuid():
    t = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # 生成 16 位随机字符串
    e = "".join(random.choice(t) for _ in range(16))
    return e

def get_snaker_id():
    return random_uuid()

def get_hm_account():
    headers = {
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
    url = "https://hm.baidu.com/hm.js?b966fe201514832da03dcf6cbf25b8a2"

    response = requests.get(url, headers=headers)
    result = re.search(r".*hca:'(.*?)',", response.text).group(1)
    return result

"""
以下是全是关于 gdxidpyhxde 值的计算部分
下面五个是变量是映射表，非常重要
"""
_0x14d460 = [
    {
        "h": "window",
        "c": "0000",
        "i": True
    },
    {
        "h": "document",
        "c": "0001",
        "i": True
    },
    {
        "h": "navigator",
        "c": "0002",
        "i": True
    },
    {
        "h": "location",
        "c": "0003",
        "i": True
    },
    {
        "h": "history",
        "c": "0004",
        "i": True
    },
    {
        "h": "screen",
        "c": "0007",
        "i": True
    },
    {
        "h": "parent",
        "c": "0008",
        "i": True
    },
    {
        "h": "top",
        "c": "0009",
        "i": True
    },
    {
        "h": "self",
        "c": "0010",
        "i": True
    },
    {
        "h": "parseFloat",
        "c": "0100",
        "i": True
    },
    {
        "h": "parseInt",
        "c": "0101",
        "i": True
    },
    {
        "h": "decodeURI",
        "c": "0102",
        "i": True
    },
    {
        "h": "decodeURIComponent",
        "c": "0103",
        "i": True
    },
    {
        "h": "encodeURI",
        "c": "0104",
        "i": True
    },
    {
        "h": "encodeURIComponent",
        "c": "0105",
        "i": True
    },
    {
        "h": "escape",
        "c": "0106",
        "i": True
    },
    {
        "h": "unescape",
        "c": "0107",
        "i": True
    },
    {
        "h": "eval",
        "c": "0108",
        "i": True
    },
    {
        "h": "_phantom",
        "c": "0200",
        "i": False
    },
    {
        "h": "callPhantom",
        "c": "0201",
        "i": False
    },
    {
        "h": "phantom",
        "c": "0202",
        "i": False
    },
    {
        "h": "phantom.injectJs",
        "c": "0203",
        "i": False
    },
    {
        "h": "context.hashCode",
        "c": "0211",
        "i": False
    }
]
_0x2aea44 = [
    "",
    "GrayText",
    "parent",
    "幼圆",
    "plugins",
    "AdobeExManDetect",
    "0010",
    "Google Earth Plugin",
    "Veetle TV Core",
    "0007",
    "0004",
    "0002",
    "0003",
    "0000",
    "0001",
    "Unity Player",
    "Skype Web Plugin",
    "WebKit-integrierte PDF",
    "gdxidpyhxdE",
    "Bell MT",
    "0008",
    "getSupportedExtensions",
    "0009",
    "SafeSearch",
    "setTime",
    "appendChild",
    "\"",
    "$",
    "Univers",
    "%",
    "&",
    "'",
    "1110",
    "get plugin string exception",
    "ThreeDShadow",
    "+",
    ",",
    "-",
    "Arab",
    "苹果丽细宋",
    ".",
    "FUZEShare",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "仿宋_GB2312",
    "5",
    "6",
    "InactiveCaptionText",
    "7",
    "WEBZEN Browser Extension",
    "8",
    "9",
    "DivX Browser Plug-In",
    ":",
    ";",
    "Uplay PC",
    "=",
    "canvas exception",
    "A",
    "B",
    "C",
    "D",
    "E",
    "微软雅黑",
    "F",
    "Harrington",
    "G",
    "H",
    "I",
    "J",
    "Gnome Shell Integration",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "Niagara Solid",
    "T",
    "SefClient Plugin",
    "U",
    "V",
    "1111",
    "W",
    "X",
    "Y",
    "Z",
    "Goudy Old Style",
    "\\",
    "Roblox Launcher Plugin",
    "Microsoft Office 2013",
    "QQMusic",
    "a",
    "Eurostile",
    "b",
    "rmocx.RealPlayer G2 Control.1",
    "c",
    "Scripting.Dictionary",
    "d",
    "仿宋",
    "e",
    "f",
    "g",
    "h",
    "Ma-Config.com plugin",
    "i",
    "1010",
    "Casual",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "1008",
    "doNotTrack",
    "q",
    "ct",
    "丽宋 Pro",
    "r",
    "setTimeout",
    "Gisha",
    "getTimezoneOffset",
    "s",
    "1005",
    "1004",
    "t",
    "1003",
    "u",
    "v",
    "1001",
    "w",
    "x",
    "drawArrays",
    "y",
    "z",
    "{",
    "}",
    "~",
    "font",
    "1009",
    "suffixes",
    "=null; path=/; expires=",
    "Shell.UIHelper",
    "toDataURL",
    "WindowText",
    "language",
    "丽黑 Pro",
    "do",
    "HighlightText",
    "div",
    "MenuText",
    "AOL Media Playback Plugin",
    "Citrix online plug-in",
    "ec",
    "Desdemona",
    "InactiveBorder",
    "RealPlayer",
    ", 'code':",
    "HELLO",
    "npTongbuAddin",
    "em",
    "createElement",
    "phantom",
    "MS PMincho",
    "楷体",
    "eval",
    "ex",
    "DivX VOD Helper Plug-in",
    "新细明体",
    "QuickTimeCheckObject.QuickTimeCheck.1",
    "FlyOrDie Games Plugin",
    "attachShader",
    "PlayOn Plug-in",
    "getTime",
    "1.01",
    "Broadway",
    "fp",
    "Alawar NPAPI utils",
    "Forte",
    "hashCode",
    "方正姚体",
    "ESN Sonar API",
    "HPDetect",
    "Bitdefender QuickScan",
    "IE Tab plugin",
    "ButtonFace",
    "',",
    "cpuClass",
    "message",
    "Century Gothic",
    "Online Storage plug-in",
    "Safer Update",
    "Msxml2.DOMDocument",
    "Engravers MT",
    "Silverlight Plug-In",
    "Google Gears 0.5.33.0",
    "Citrix ICA Client",
    "alphabetic",
    "context",
    "VDownloader",
    "华文楷体",
    "attrVertex",
    "宋体",
    "cookie",
    "%22",
    "%26",
    "Centaur",
    "4game",
    "Rockwell",
    "LogMeIn Plugin 1.0.0.961",
    "Octoshape Streaming Services",
    "toGMTString",
    "th=/",
    "SumatraPDF Browser Plugin",
    "PDF.PdfCtrl",
    "fillStyle",
    "fontSize",
    "Adobe Ming Std",
    "je",
    "TorchHelper",
    "Franklin Gothic Heavy",
    "华文仿宋",
    "Harmony Plug-In",
    "Gigi",
    "v1.1",
    "Kino MT",
    "SimHei",
    "AliSSOLogin plugin",
    "RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)",
    "Yandex PDF Viewer",
    "Citrix Receiver Plug-in",
    "top",
    "mai",
    "AcroPDF.PDF",
    "canvas api exception",
    "InactiveCaption",
    "Menu",
    "precision mediump float; varying vec2 varyinTexCoordinate; void main() {   gl_FragColor = vec4(varyinTexCoordinate, 0, 1); }",
    "QQ2013 Firefox Plugin",
    "Google Update",
    "华文彩云",
    "eMusicPlugin DLM6",
    "Web Components",
    "Babylon ToolBar",
    "Coowon Update",
    "InfoText",
    "rmocx.RealPlayer G2 Control",
    "iMesh plugin",
    "RealDownloader Plugin",
    "Symantec PKI Client",
    "_phantom",
    "GDL Object Web Plug-in 16.00",
    "webgl",
    "华文宋体",
    "screen",
    "body",
    "TRIANGLE_STRIP",
    "TlwgMono",
    "n=",
    "LogMeIn Plugin 1.0.0.935",
    "':'",
    "function",
    "context.hashCode",
    "ArchiCAD",
    "VERTEX_SHADER",
    "Ubuntu",
    "Facebook Plugin",
    "ActiveCaption",
    "细明体",
    "Malgun Gothic",
    "News Gothic MT",
    "CaptionText",
    "aZbY0cXdW1eVf2Ug3Th4SiR5jQk6PlO7mNn8MoL9pKqJrIsHtGuFvEwDxCyBzA",
    "DejaVu LGC Sans Mono",
    "Copperplate Gothic Light",
    "Segoe Print",
    "Sawasdee",
    "Bauhaus 93",
    "Chalkduster",
    "Abadi MT Condensed Light",
    "Lucida Bright",
    "Wide Latin",
    "font detect error",
    "Kozuka Gothic Pr6N",
    "Html5 location provider",
    "DivX Plus Web Player",
    "Vladimir Script",
    "File Downloader Plug-in",
    "ob",
    "Adodb.Stream",
    "Menlo",
    "callPhantom",
    "Wolfram Mathematica",
    "CatalinaGroup Update",
    "Eras Bold ITC",
    "DevalVRXCtrl.DevalVRXCtrl.1",
    "华文细黑",
    "addBehavior",
    "pa",
    "Bitstream Vera Serif",
    "(function(){return 123;})();",
    "pi",
    "Tencent FTN plug-in",
    "removeChild",
    "Folx 3 Browser Plugin",
    "useProgram",
    "hostname",
    "phantom.injectJs",
    "ShockwaveFlash.ShockwaveFlash",
    "height",
    "rgba(102, 204, 0, 0.7)",
    "AdblockPlugin",
    "Background",
    "AgControl.AgControl",
    "PhotoCenterPlugin1.1.2.2",
    "GungSeo",
    "s=",
    "decodeURI",
    "方正舒体",
    "华文新魏",
    "123",
    "webgl exception",
    "re",
    "WMPlayer.OCX",
    "72px",
    "AppWorkspace",
    "Highlight",
    "document",
    "Yandex Media Plugin",
    "ESN Launch Mozilla Plugin",
    "70px 'Arial'",
    "injectJs",
    "Loma",
    "BitCometAgent",
    "Calibri",
    "Bookman Old Style",
    "sessionStorage",
    "Utopia",
    "compileShader",
    "escape",
    "Scrollbar",
    "Window",
    "隶书",
    "Kaspersky Password Manager",
    "MingLiU-ExtB",
    "get system colors exception",
    "Skype.Detection",
    "FileLab plugin",
    "npAPI Plugin",
    "not_exist_host",
    "2d",
    "ActiveXObject",
    "Dotum",
    "PDF-XChange Viewer",
    "offsetHeight",
    "PMingLiU",
    "colorDepth",
    "Nokia Suite Enabler Plugin",
    "RealVideo.RealVideo(tm) ActiveX Control (32-bit)",
    "Magneto",
    "AdobeExManCCDetect",
    "Gabriola",
    "Playbill",
    "navigator",
    "Rachana",
    "Tw Cen MT Condensed Extra Bold",
    "QQMiniDL Plugin",
    "#f60",
    "fillRect",
    "Default Browser Helper",
    "=null; path=/; domain=",
    "French Script MT",
    "标楷体",
    "encodeURI",
    "Umpush",
    "icp",
    "华文琥珀",
    "createProgram",
    "monospace",
    "ButtonShadow",
    "Bodoni MT",
    "STATIC_DRAW",
    "黑体",
    "downloadUpdater",
    "Aliedit Plug-In",
    "PDF integrado do WebKit",
    "uniformOffset",
    "encodeURIComponent",
    "Picasa",
    "Adobe Fangsong Std",
    "bindBuffer",
    "AVG SiteSafety plugin",
    "Orbit Downloader",
    "color",
    "hidden",
    "localStorage",
    "Google Talk Effects Plugin",
    "description",
    "indexedDB",
    "Lucida Fax",
    "AmazonMP3DownloaderPlugin",
    "createBuffer",
    "Castellar",
    "linkProgram",
    "Californian FB",
    "ThreeDHighlight",
    "createShader",
    "Gulim",
    "NyxLauncher",
    "YouTube Plug-in",
    "楷体_GB2312",
    "SWCtl.SWCtl",
    "Google Earth Plug-in",
    "QQDownload Plugin",
    "Norton Identity Safe",
    "parseInt",
    "Simple Pass",
    "Colonna MT",
    "zako",
    "getUniformLocation",
    "shaderSource",
    "Downloaders plugin",
    "location",
    "Heroes & Generals live",
    "window",
    "Showcard Gothic",
    "微软正黑体",
    "华文行楷",
    "Ginger",
    "RockMelt Update",
    "WindowFrame",
    "enableVertexAttribArray",
    "KacstOne",
    "attribute vec2 attrVertex; varying vec2 varyinTexCoordinate; uniform vec2 uniformOffset; void main() {   varyinTexCoordinate = attrVertex + uniformOffset;   gl_Position = vec4(attrVertex, 0, 1); }",
    "Perpetua",
    "openDatabase",
    "canvas",
    "iGetterScriptablePlugin",
    "Informal Roman",
    "Nitro PDF Plug-In",
    "Msxml2.XMLHTTP",
    "华文黑体",
    "NPLastPass",
    "ThreeDFace",
    "style",
    "LastPass",
    "::",
    "parseFloat",
    "华文隶书",
    "; ",
    "getAttribLocation",
    "{'name':",
    "Nyala",
    "not_exist_hostname",
    "\\'",
    "GFACE Plugin",
    "undefined",
    "新宋体",
    "\\.",
    "Matura MT Script Capitals",
    "Arial Black",
    "FangSong",
    "mwC nkbafjord phsgly exvt zqiu, ὠ tphst/:/uhbgtic.mo/levva",
    "Braggadocio",
    "Harmony Firefox Plugin",
    "Palace Script MT",
    "Native Client",
    "offsetWidth"
]
_0x3a102c = [
    36,
    28,
    51,
    9,
    23,
    7,
    0,
    2,
    1423857449,
    -2,
    3,
    -3,
    3432918353,
    1555261956,
    4,
    2847714899,
    -4,
    5,
    -5,
    2714866558,
    1281953886,
    6,
    -6,
    198958881,
    1141124467,
    2970347812,
    -7,
    7,
    3110523913,
    8,
    -8,
    2428444049,
    -9,
    9,
    10,
    -10,
    -11,
    11,
    2563907772,
    -12,
    12,
    13,
    2282248934,
    -13,
    2154129355,
    -14,
    14,
    15,
    -15,
    16,
    -16,
    17,
    -17,
    -18,
    18,
    19,
    -19,
    20,
    -20,
    21,
    -21,
    -22,
    22,
    -23,
    23,
    24,
    -24,
    25,
    -25,
    -26,
    26,
    27,
    -27,
    28,
    -28,
    29,
    -29,
    30,
    -30,
    31,
    -31,
    33,
    -33,
    -32,
    32,
    -34,
    -35,
    34,
    35,
    37,
    -37,
    36,
    -36,
    38,
    39,
    -39,
    -38,
    40,
    41,
    -41,
    -40,
    42,
    -43,
    -42,
    43,
    45,
    -45,
    -44,
    44,
    47,
    -46,
    -47,
    46,
    48,
    -49,
    -48,
    49,
    -50,
    51,
    -51,
    50,
    570562233,
    53,
    -52,
    52,
    -53,
    -54,
    -55,
    55,
    54,
    503444072,
    57,
    -56,
    -57,
    56,
    59,
    58,
    -59,
    -58,
    60,
    61,
    -61,
    -60,
    62,
    63,
    -63,
    -62,
    -64,
    711928724,
    -66,
    67,
    -65,
    65,
    -67,
    66,
    64,
    -71,
    -69,
    69,
    68,
    70,
    -68,
    -70,
    71,
    -72,
    3686517206,
    -74,
    -73,
    73,
    75,
    74,
    -75,
    72,
    -79,
    76,
    79,
    78,
    -78,
    -76,
    77,
    -77,
    3554079995,
    -81,
    81,
    -82,
    -83,
    80,
    -80,
    82,
    83,
    -84,
    84,
    85,
    -86,
    -87,
    86,
    -85,
    87,
    90,
    -88,
    -89,
    -90,
    88,
    89,
    91,
    -91,
    94,
    92,
    95,
    -94,
    93,
    -93,
    -95,
    -92,
    -98,
    97,
    98,
    -97,
    -99,
    96,
    99,
    -96,
    -100,
    3272380065,
    102,
    -102,
    -101,
    -103,
    103,
    100,
    101,
    -107,
    -104,
    105,
    104,
    106,
    -106,
    -105,
    107,
    109,
    -109,
    -108,
    -111,
    110,
    -110,
    111,
    108,
    251722036,
    115,
    -115,
    112,
    -114,
    -112,
    113,
    114,
    -113,
    -117,
    119,
    -116,
    -119,
    117,
    -118,
    118,
    116,
    123,
    -120,
    122,
    -121,
    120,
    -122,
    -123,
    121,
    125,
    127,
    3412177804,
    -127,
    126,
    -126,
    124,
    -125,
    -124,
    -128,
    128,
    -129,
    1843258603,
    3803740692,
    984961486,
    3939845945,
    4195302755,
    4066508878,
    255,
    1706088902,
    256,
    1969922972,
    2097651377,
    376229701,
    853044451,
    752459403,
    426522225,
    1000,
    3772115230,
    615818150,
    3904427059,
    4167216745,
    4027552580,
    3654703836,
    1886057615,
    879679996,
    3518719985,
    3244367275,
    2013776290,
    3373015174,
    1759359992,
    285281116,
    1622183637,
    1006888145,
    1231636301,
    10000,
    83908371,
    1090812512,
    2463272603,
    1373503546,
    2596254646,
    2321926636,
    1504918807,
    2181625025,
    2882616665,
    2747007092,
    3009837614,
    3138078467,
    397917763,
    81470997,
    829329135,
    2657392035,
    956543938,
    2517215374,
    2262029012,
    40735498,
    2394877945,
    3266489909,
    702138776,
    2808555105,
    2936675148,
    1258607687,
    1131014506,
    3218104598,
    3082640443,
    1404277552,
    565507253,
    534414190,
    1541320221,
    1913087877,
    2053790376,
    1789927666,
    3965973030,
    3826175755,
    4107580753,
    4240017532,
    1658658271,
    3579855332,
    3708648649,
    3453421203,
    3317316542,
    1873836001,
    1742555852,
    461845907,
    3608007406,
    1996959894,
    3747672003,
    3485111705,
    2137656763,
    3352799412,
    213261112,
    3993919788,
    1.01,
    3865271297,
    4139329115,
    4275313526,
    282753626,
    1068828381,
    2768942443,
    2909243462,
    936918000,
    3183342108,
    27492,
    141376813,
    3050360625,
    654459306,
    2617837225,
    1454621731,
    2489596804,
    2227061214,
    1591671054,
    2362670323,
    4294967295,
    1308918612,
    2246822507,
    795835527,
    1181335161,
    414664567,
    4279200368,
    1661365465,
    1037604311,
    4150417245,
    3887607047,
    1802195444,
    4023717930,
    2075208622,
    1943803523,
    901097722,
    628085408,
    755167117,
    3322730930,
    3462522015,
    3736837829,
    3604390888,
    2366115317,
    0.4,
    2238001368,
    2512341634,
    2647816111,
    -0.2,
    314042704,
    1510334235,
    900000,
    58964,
    1382605366,
    31158534,
    450548861,
    3020668471,
    1119000684,
    3160834842,
    2898065728,
    1256170817,
    2765210733,
    3060149565,
    3188396048,
    2932959818,
    124634137,
    2797360999,
    366619977,
    62317068,
    -0.26,
    1202900863,
    498536548,
    1340076626,
    2405801727,
    2265490386,
    1594198024,
    1466479909,
    2547177864,
    249268274,
    2680153253,
    2125561021,
    3294710456,
    855842277,
    3423369109,
    0.732134444,
    3705015759,
    3569037538,
    1994146192,
    1711684554,
    1852507879,
    997073096,
    733239954,
    4251122042,
    601450431,
    4111451223,
    167816743,
    3855990285,
    3988292384,
    3369554304,
    3233442989,
    3495958263,
    3624741850,
    65535,
    453092731,
    -0.9,
    2094854071,
    1957810842,
    325883990,
    4057260610,
    1684777152,
    4189708143,
    3915621685,
    162941995,
    1812370925,
    3775830040,
    783551873,
    3134207493,
    1172266101,
    2998733608,
    2724688242,
    1303535960,
    2852801631,
    112637215,
    1567103746,
    651767980,
    1426400815,
    906185462,
    2211677639,
    1047427035,
    2344532202,
    2607071920,
    2466906013,
    225274430,
    544179635,
    2176718541,
    2312317920,
    1483230225,
    1342533948,
    2567524794,
    2439277719,
    1088359270,
    671266974,
    1219638859,
    840000,
    953729732,
    3099436303,
    2966460450,
    817233897,
    2685067896,
    2825379669,
    4089016648,
    4224994405,
    3943577151,
    3814918930,
    476864866,
    1634467795,
    335633487,
    1762050814,
    1,
    2044508324,
    -1,
    3401237130,
    3268935591,
    3524101629,
    3663771856,
    1907459465
]
_0x275425 = [
    "userAgent",
    "QuickTime.QuickTime",
    "experimental-webgl",
    "ARRAY_BUFFER",
    "苹果丽中黑",
    "Alipay Security Control 3",
    "Script MT Bold",
    ", 'browserProp':",
    "TDCCtl.TDCCtl",
    "width",
    "self",
    "InfoBackground",
    "Pando Web Plugin",
    "Haettenschweiler",
    "span",
    "innerHTML",
    "ActiveBorder",
    "ThreeDLightShadow",
    "0202",
    "0203",
    "fontFamily",
    "0200",
    "0201",
    "WPI Detector 1.4",
    "; expires=",
    "ThreeDDarkShadow",
    "Exif Everywhere",
    "Battlelog Game Launcher",
    "Impact",
    "VLC Multimedia Plugin",
    "Adobe Hebrew",
    "BlueStacks Install Detector",
    "wwwmmmmmmmmmmlli",
    "history",
    "sans-serif",
    "14731255234d414cF91356d684E4E8F5F56c8f1bc",
    "Papyrus",
    "ButtonText",
    "0211",
    "AppUp",
    "Parom.TV player plugin",
    "DealPlyLive Update",
    "Lohit Gujarati",
    "FRAGMENT_SHADER",
    "Agency FB",
    "MacromediaFlashPaper.MacromediaFlashPaper",
    "###",
    "WordCaptureX",
    "getComputedStyle",
    "platform",
    "0105",
    "Arabic Typesetting",
    "0106",
    "0103",
    "华文中宋",
    "0104",
    "0101",
    "0102",
    "0100",
    "0107",
    "ButtonHighlight",
    "vertexAttribPointer",
    "0108",
    "textBaseline",
    "#069",
    "doubleTwist Web Plugin",
    "match",
    "unescape",
    "Thunder DapCtrl NPAPI Plugin",
    "Batang",
    "DFKai-SB",
    "Snap ITC",
    "MinibarPlugin",
    "Date",
    "decodeURIComponent",
    "NPPlayerShell",
    "MS Reference Sans Serif",
    "Hiragino Sans GB",
    "serif",
    "getContext",
    "uniform2f",
    "MoolBoran"
]
_0x5d3a89 = [
    -9,
    -84,
    -50,
    59,
    115,
    102,
    57,
    125,
    94,
    -15,
    15,
    2,
    -72,
    -98,
    -79,
    38,
    -56,
    -49,
    76,
    -26,
    -117,
    60,
    90,
    9,
    -107,
    -12,
    -71,
    -100,
    63,
    42,
    -18,
    28,
    -120,
    -11,
    33,
    45,
    79,
    92,
    37,
    97,
    4,
    58,
    98,
    84,
    -97,
    -88,
    95,
    -104,
    -13,
    -89,
    78,
    -90,
    119,
    -66,
    13,
    -5,
    29,
    -116,
    -4,
    -81,
    27,
    40,
    -59,
    -43,
    85,
    48,
    -74,
    109,
    -64,
    26,
    67,
    -33,
    -115,
    0,
    -37,
    -102,
    88,
    -48,
    127,
    -86,
    41,
    105,
    -2,
    122,
    -42,
    112,
    -94,
    81,
    -31,
    -65,
    -101,
    -14,
    65,
    49,
    -67,
    -114,
    -103,
    -87,
    -19,
    104,
    66,
    -73,
    -34,
    -78,
    -45,
    -27,
    -109,
    -108,
    47,
    61,
    86,
    43,
    -54,
    25,
    64,
    -35,
    -44,
    53,
    -112,
    36,
    73,
    89,
    -82,
    51,
    -32,
    39,
    -83,
    80,
    -85,
    -111,
    12,
    -58,
    103,
    -76,
    -46,
    -127,
    34,
    1,
    -99,
    14,
    -57,
    110,
    106,
    93,
    -52,
    11,
    113,
    20,
    -106,
    75,
    62,
    -69,
    -39,
    -55,
    -119,
    126,
    114,
    123,
    10,
    77,
    -121,
    -8,
    74,
    21,
    -93,
    17,
    -61,
    -21,
    -105,
    -126,
    18,
    124,
    -17,
    52,
    -10,
    -77,
    -24,
    -22,
    120,
    -95,
    -25,
    96,
    -110,
    22,
    -23,
    69,
    -125,
    -128,
    -47,
    -38,
    -1,
    3,
    -20,
    100,
    68,
    101,
    5,
    117,
    -122,
    44,
    -51,
    -36,
    -41,
    24,
    -80,
    30,
    82,
    -63,
    -40,
    -92,
    91,
    -6,
    -53,
    -124,
    -62,
    -28,
    111,
    19,
    50,
    108,
    70,
    -68,
    -29,
    -75,
    99,
    -91,
    -60,
    -70,
    71,
    -118,
    -3,
    83,
    87,
    -7,
    32,
    55,
    31,
    -123,
    121,
    107,
    -113,
    46,
    -30,
    118,
    54,
    23,
    116,
    -16,
    7,
    6,
    35,
    16,
    -96,
    56,
    72,
    8
]

# 随机加盐
def _0x3f6f3f(_length):
    alphabet = "aZbY0cXdW1eVf2Ug3Th4SiR5jQk6PlO7mNn8MoL9pKqJrIsHtGuFvEwDxCyBzA"
    return ''.join(random.choice(alphabet) for _ in range(_length))

# 该方法没有用上
def _0x1c8398(_0x3d6d24):
    _0x1799d2 = [_0x2aea44[0x89], _0x2aea44[0xb9], _0x2aea44[0x88], _0x2aea44[0x6e], _0x2aea44[0xa2], _0x2aea44[0xa9],
                 _0x2aea44[0x180]]
    _0x156928 = '{'
    for _ in _0x1799d2:
        if _ in _0x3d6d24:
            _0x156928 += "'" + _ + "':'" + _0x3d6d24[_] + "',"
    return _0x156928[:-1] + '}'

# 没有用上
def _0x4178ff(_0x46cfdd):
    return [ord(_) for _ in _0x46cfdd]

# 标准 CRC32 计算，返回 16 进制
def standard_crc32(data_bytes):
    return "%08x" % (zlib.crc32(data_bytes) & 0xFFFFFFFF)

def _0x10df53(_0x4e8c7f):
    return (_0x4e8c7f + 128) % 256 - 128

def _0x34a415(_0x1c42ee):
    _0x4bd1db = []
    if len(_0x1c42ee) >= 64:
        if _0x1c42ee and len(_0x1c42ee) > 0:
            for _ in range(64):
                _0x4bd1db.append(_0x1c42ee[_])
            return _0x4bd1db
    for _ in range(64):
        _0x4bd1db.append(_0x1c42ee[_ % len(_0x1c42ee)])
    return _0x4bd1db

def _0x3346f1(_0x8bede2, _0x3763c1):
    x = _0x10df53(_0x8bede2)
    y = _0x10df53(_0x3763c1)
    return _0x10df53(x ^ y)

def _0x314b89(_0x251f87, _0x2650b3):
    _0x121ded = []
    for x, y in zip(_0x251f87, _0x2650b3):
        _0x121ded.append(_0x3346f1(x, y))
    return _0x121ded

def _0x538bb0(_0x462a02):
    _0x2ec9b2 = [(_0x462a02 >> _0x3a102c[0x41]) & _0x3a102c[0x122],
                 (_0x462a02 >> _0x3a102c[0x31]) & _0x3a102c[0x122],
                 (_0x462a02 >> _0x3a102c[0x1d]) & _0x3a102c[0x122],
                 _0x462a02 & _0x3a102c[0x122]]
    return _0x2ec9b2

def _0x2055e1(_0xb031b3, _0x2a082d):
    x = _0x10df53(_0xb031b3)
    y = _0x10df53(_0x2a082d)
    return _0x10df53(x + y)

def _0x474f75(_0x251f87, _0x2650b3):
    _0x121ded = []
    for x, y in zip(_0x251f87, _0x2650b3):
        _0x121ded.append(_0x2055e1(x, y))
    return _0x121ded

def _0x45222a(_0x46fcd5):
    _0x424296 = []
    for _ in _0x46fcd5:
        val = _ & 0xFF
        index = ((val >> 4) & 0xF) * 16 + (val & 0xF)
        _0x424296.append(_0x5d3a89[index])
    return _0x424296

# 魔改版 base64
def _0x3d9f27(data_array, offset, chunk_size):
    alphabet = [
        "2", "4", "0", "a", "Y", "H", "i", "Q", "x", "L", "\\", "Z", "u", "f", "V", "l",
        "g", "8", "s", "P", "M", "R", "6", "d", "G", "k", "X", "v", "O", "/", "C", "b",
        "w", "9", "W", "D", "j", "1", "E", "T", "y", "I", "S", "c", "m", "e", "o", "J",
        "z", "3", "7", "q", "t", "h", "B", "r", "U", "+", "K", "N", "A", "5", "p", "n"
    ]

    padding_char = "F"

    res = []

    # 无论 chunk_size 是 1, 2 还是 3，逻辑都要覆盖
    b1 = data_array[offset]
    b2 = data_array[offset + 1] if chunk_size > 1 else 0
    b3 = data_array[offset + 2] if chunk_size > 2 else 0

    # 1. 字符 1 (始终存在)
    res.append(alphabet[(b1 >> 2) & 0x3F])

    # 2. 字符 2 (始终存在)
    res.append(alphabet[((b1 << 4) & 0x30) | ((b2 >> 4) & 0x0F)])

    # 3. 字符 3 (如果只有 1 字节，这里就是填充符)
    if chunk_size > 1:
        res.append(alphabet[((b2 << 2) & 0x3C) | ((b3 >> 6) & 0x03)])
    else:
        res.append(padding_char)

    # 4. 字符 4 (如果只有 1 或 2 字节，这里就是填充符)
    if chunk_size > 2:
        res.append(alphabet[b3 & 0x3F])
    else:
        res.append(padding_char)

    return "".join(res)

# 如果 cookie 需要带上 expires 则用这个方法
def _0x5a1052(_0x4ca654, _0x4bed87, _0x55dbed):
    _0x194953 = _0x4ca654 + '=' + encode_uri_component(_0x4bed87) +\
        '; expires=' +\
        datetime.fromtimestamp(_0x55dbed / 1000.0, tz=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT') +\
        '; path=/'
    return _0x194953

def _0x28c2a9():
    _0x1d3f57 = int(time.time() * 1000) + 900000
    _0x5a0e0d = _0x1d3f57 + 1000 * 60 * 60 * 24 * 30
    _0x548794 = {
        "v": "v1.1",
        'fp': ','.join(["11064002021626", "16559845875841"]),
        'u': _0x3f6f3f(3) + str(_0x1d3f57) + _0x3f6f3f(3),
        'h': 'ctbpsp.com',
    }
    _0x11ee50 = _0x155fa5 = str(_0x548794).replace(' ', '')
    _0xd4eb7e = standard_crc32(_0x11ee50.encode())
    _0x548794 = _0x275425[0x23]
    _0x511709 = _0x4178ff(_0x11ee50 + _0xd4eb7e)
    _0x9a4441 = _0x4178ff(_0x548794)
    _0xd4eb7e = [_0x10df53(random.randint(0, 255)) for _ in range(4)]
    _0x9a4441 = _0x34a415(_0x9a4441)
    _0x9a4441 = _0x314b89(_0x9a4441, _0x34a415(_0xd4eb7e))
    _0x17f108 = _0x9a4441 = _0x34a415(_0x9a4441)
    _0x462e32 = _0x511709

    _0x92b403 = len(_0x462e32)
    remainder = _0x92b403 % 64
    if remainder <= 60:
        _0x51546e = 64 - remainder - 4
    else:
        _0x51546e = 64 * 2 - remainder - 4
    _0x511709 = _0x462e32.copy()
    for _ in range(_0x51546e):
        _0x511709.append(0)
    _0x28e797 = _0x538bb0(_0x92b403)
    _0x511709 += _0x28e797
    _0x539a57 = _0x511709

    _0x92b403 = _0x539a57
    _0x539a57 = []
    for i in range(len(_0x92b403) // 64):
        _0x539a57.append(_0x92b403[i * 64:(i + 1) * 64])
    _0x18d3ae = _0xd4eb7e
    for _ in _0x539a57:
        _0x215aa7 = _
        _0x56f8a1 = _0x10df53(37)
        _0x46092d = []
        for k in _0x215aa7:
            _0x46092d.append(_0x3346f1(k, _0x56f8a1))
        _0x19193b = _0x46092d

        _0x46092d = _0x19193b
        _0x4ade5a = _0x10df53(35)
        _0x63c3c5 = []
        for k in _0x46092d:
            _0x63c3c5.append(_0x3346f1(k, _0x4ade5a))
            _0x4ade5a -= 1
        _0x2573f1 = _0x63c3c5

        _0x46092d = _0x2573f1
        _0x5de767 = _0x10df53(-44)
        _0x63c3c5 = []
        for k in _0x46092d:
            _0x63c3c5.append(_0x2055e1(k, _0x5de767))
            _0x5de767 += 1
        _0x74a09a = _0x63c3c5
        _0x47be8c = _0x314b89(_0x74a09a, _0x9a4441)

        _0x46092d = _0x47be8c
        _0x63c3c5 = _0x17f108
        _0x16fc88 = len(_0x63c3c5)
        _0x3cbf3d = []
        for k in range(len(_0x46092d)):
            _0x3cbf3d.append(_0x10df53(_0x46092d[k] + _0x63c3c5[k % _0x16fc88]))
        _0x13ad86 = _0x3cbf3d

        _0x47be8c = _0x314b89(_0x13ad86, _0x17f108)
        _0x4d5154 = _0x45222a(_0x47be8c)
        _0x4d5154 = _0x45222a(_0x4d5154)
        _0x18d3ae += _0x4d5154
        _0x17f108 = _0x4d5154

    _0x2eadd2 = ''
    for _ in range(0, len(_0x18d3ae), 3):
        _0x2eadd2 += _0x3d9f27(_0x18d3ae, _, 3)
    _0x155fa5 = _0x2eadd2 + ':' + str(_0x1d3f57)
    _0x4d1cfd = _0x2aea44[0x12]
    # return _0x5a1052(_0x4d1cfd, _0x155fa5, _0x5a0e0d)
    return encode_uri_component(_0x155fa5)

def get_gdxidpyhxde():
    return _0x28c2a9()

def uuid(_0x5aa56e):
    _0x171c6a = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return ''.join([random.choice(_0x171c6a) for _ in range(_0x5aa56e)])

def _0x5023e1(_0x4d549e):
    _0x4b0021 = {
        '\\': '-',
        '/': '_',
        '+': '*'
    }
    _0x40c0f0 = _0x4b0021
    return re.sub(r'[\\/+]', lambda _0xe86ca2: _0x40c0f0[_0xe86ca2.group()], _0x4d549e)

def _0x37afb7():
    _0x38f130 = 'fd6a43ae25f74398b61c03c83be37449'
    _0x226bcd = list(_0x38f130.encode())
    _0x2428ae = [_0x10df53(random.randint(0, 255)) for _ in range(4)]
    _0x226bcd = _0x34a415(_0x226bcd)
    _0x226bcd = _0x314b89(_0x226bcd, _0x34a415(_0x2428ae))
    _0x226bcd = _0x34a415(_0x226bcd)
    return [_0x226bcd, _0x2428ae]

def _0x5dfb84(data_list):
    data_len = len(data_list)
    # 1. 如果数据为空，返回 64 字节全 0 列表
    if data_len == 0:
        return [0] * 64
    # 2. 计算填充 0 的个数 (预留 4 字节存长度)
    # JS 逻辑: 0x40 - data_len % 0x40 - 4
    remainder = data_len % 64
    if remainder <= 60:
        padding_zeros = 64 - remainder - 4
    else:
        padding_zeros = 128 - remainder - 4

    # 3. 构建新数组
    # 先放入原始数据
    padded_data = list(data_list)
    # 放入填充的 0
    padded_data.extend([0] * padding_zeros)

    length_bytes = [
        (data_len >> 24) & 0xFF,
        (data_len >> 16) & 0xFF,
        (data_len >> 8) & 0xFF,
        data_len & 0xFF
    ]
    padded_data.extend(length_bytes)
    return padded_data

def _0x541d79(data_list):
    if len(data_list) % 64 != 0:
        return []
    blocks = []
    for i in range(0, len(data_list), 64):
        block = data_list[i: i + 64]
        blocks.append(block)
    return blocks

def _0x1ca2ea(hex_pair):
    hex_pair = str(hex_pair)
    high_nibble = int(hex_pair[0], 16) << 4
    low_nibble = int(hex_pair[1], 16)
    return _0x10df53(high_nibble + low_nibble)

def _0x5995f1(data_list, key):
    if not data_list:
        return []
    current_key = _0x10df53(key)
    _0x558c8d = []
    for byte in data_list:
        _0x558c8d.append(_0x3346f1(byte, current_key))
        current_key = _0x10df53(current_key + 1)
    return _0x558c8d

def _0x446610(data_list, key):
    if not data_list:
        return []
    current_key = _0x10df53(key)
    _0x558c8d = []
    for byte in data_list:
        _0x558c8d.append(_0x2055e1(byte, current_key))
        current_key = _0x10df53(current_key + 1)
    return _0x558c8d

def _0x23c1c7(data_list, key):
    if not data_list:
        return []
    current_key = _0x10df53(key)
    _0x558c8d = []
    for byte in data_list:
        _0x558c8d.append(_0x2055e1(byte, current_key))
        current_key = _0x10df53(current_key - 1)
    return _0x558c8d

def _0x20f9c7(data_list, key):
    if not data_list:
        return []
    current_key = _0x10df53(key)
    _0x558c8d = []
    for byte in data_list:
        _0x558c8d.append(_0x3346f1(byte, current_key))
        current_key = _0x10df53(current_key - 1)
    return _0x558c8d

def _0x1d8917(data_list, key):
    if not data_list:
        return []
    current_key = _0x10df53(key)
    return [_0x2055e1(byte, current_key) for byte in data_list]

def _0x5dd6b9(data_list, key):
    if not data_list:
        return []
    current_key = _0x10df53(key)
    return [_0x3346f1(byte, current_key) for byte in data_list]

def _0x509c46(data_list, op_key=0):
    return data_list if op_key + 256 >= 0 else []

def _0x34ece2(_0x504715):
    _0x6c64fe = [_0x509c46, _0x5dd6b9, _0x1d8917, _0x5995f1, _0x446610, _0x20f9c7, _0x23c1c7]
    _0x1879be = '037606da0296055c'
    for _ in range(0, len(_0x1879be), 4):
        _0x3488ec = _0x1879be[_: _ + 4]
        _0x17acd8 = _0x1ca2ea(_0x3488ec[0: 2])
        _0x2af631 = _0x1ca2ea(_0x3488ec[2: 4])
        _0x504715 = _0x6c64fe[_0x17acd8](_0x504715, _0x2af631)
    return _0x504715

def _0x18c57a(_0x210854):
    _0x52ac6c = []
    _0x648db6 = 0
    for _ in range(0, len(_0x210854) // 2):
        _0x47cc6f = int(_0x210854[_0x648db6], 16) << 4
        _0x648db6 += 1
        _0x2eb20e = int(_0x210854[_0x648db6], 16)
        _0x648db6 += 1
        _0x52ac6c.append(_0x10df53(_0x47cc6f + _0x2eb20e))
    return _0x52ac6c

def _0x560bb0(_0xe063b1, _0x49e758):
    return _0xe063b1[16 * ((_0x49e758 & 0xFF) >> 4 & 0xF) + (0xF & _0x49e758)]

def _0x1556d2(_0x21336a):
    _0x5bf327 = "a7be3f3933fa8c5fcf86c4b6908b569ba1e26c1a6d7cfbf60ae4b00e074a194dac4b73e7f898541159a39d08183b76eedee3ed341e6685d2357440158394b1ff03a9004cbbb5ca7dcb7f41489a16e03dcc9c71eb3c9796685b1d01b4d56193a6e1f1a2470445c191ae49c5d82765dc82c350f263387a24a502fcbf442e2dddaad0e936d9ea22b89275307b42518fbc3a626ba806d4ecd6d725f50cc8c72fefa4551ccd6fc9b2b7ab954f815c7264c6e51f4eaf99885a79892b1b60a0b3526e57ba5d178d370958847eb9fd28f9ce0bc023f4148a2adfe632126769057043d3bd8eda0df7872629f3809ef05310e83113216afe202c460fc23e789f77d1addb5e"
    _0x5a7120 = _0x18c57a(_0x5bf327)
    _0x14ac5a = []
    for _ in _0x21336a:
        _0x14ac5a.append(_0x560bb0(_0x5a7120, _))
    return _0x14ac5a

def _0x2d84c6(chunk, alphabet, padding_char):
    res = []
    length = len(chunk)

    b1 = chunk[0] & 0xFF
    b2 = (chunk[1] & 0xFF) if length > 1 else 0
    b3 = (chunk[2] & 0xFF) if length > 2 else 0

    if length == 1:
        res.append(alphabet[(b1 >> 2) & 0x3F])
        res.append(alphabet[((b1 << 4) & 0x30) + ((b2 >> 4) & 0x0F)])
        res.append(padding_char)
        res.append(padding_char)
    elif length == 2:
        res.append(alphabet[(b1 >> 2) & 0x3F])
        res.append(alphabet[((b1 << 4) & 0x30) + ((b2 >> 4) & 0x0F)])
        res.append(alphabet[((b2 << 2) & 0x3C) + ((b3 >> 6) & 0x03)])
        res.append(padding_char)
    elif length == 3:
        res.append(alphabet[(b1 >> 2) & 0x3F])
        res.append(alphabet[((b1 << 4) & 0x30) + ((b2 >> 4) & 0x0F)])
        res.append(alphabet[((b2 << 2) & 0x3C) + ((b3 >> 6) & 0x03)])
        res.append(alphabet[b3 & 0x3F])
    return "".join(res)

def _0x4c4b3e(data_list, cf_key, a9_param):
    result = []
    i = 0
    total_len = len(data_list)
    while i < total_len:
        if i + 3 <= total_len:
            chunk = data_list[i: i + 3]
            transformed = _0x2d84c6(chunk, cf_key, a9_param)
            result.append(transformed)
            i += 3
        else:
            chunk = data_list[i:]
            transformed = _0x2d84c6(chunk, cf_key, a9_param)
            result.append(transformed)
            break
    return ''.join(result)

def _0x491e42(_0x5f2b73):
    _0x33d08a = 'MB.CfHUzEeJpsuGkgNwhqiSaI4Fd9L6jYKZAxn1/Vml0c5rbXRP+8tD3QTO2vWyo'
    return _0x4c4b3e(_0x5f2b73, _0x33d08a, '7')

def _0x3ebd00(_0x1b0494):
    _0x1c8e88 = _0x1b0494.encode()
    _0x45dc26 = _0x37afb7()
    _0x9181b5 = _0x45dc26
    _0x51196b = _0x9181b5[0]
    _0x334cfd = _0x9181b5[1]
    _0x28b0cc = list(standard_crc32(_0x1c8e88).encode())
    _0x519a2a = _0x5dfb84(list(_0x1c8e88) + _0x28b0cc)
    _0x5e1d80 = _0x541d79(_0x519a2a)
    _0x7fbfd6 = _0x334cfd.copy()
    _0x18fc8a = _0x51196b
    for _ in _0x5e1d80:
        _0x24a8ff = _0x314b89(_0x34ece2(_), _0x51196b)
        _0x435af1 = _0x474f75(_0x24a8ff, _0x18fc8a)
        _0x24a8ff = _0x314b89(_0x435af1, _0x18fc8a)
        _0x18fc8a = _0x1556d2(_0x1556d2(_0x24a8ff))
        _0x7fbfd6 += _0x18fc8a

    return _0x491e42(_0x7fbfd6)

def get_necaptcha(_0x3a5029, _0x4c2e3c, _0x10ac06='CN31'):
    """
    生成 NECaptcha-Validate
    :param _0x3a5029: 易盾 check 接口返回的 validate
    :param _0x4c2e3c: gdxidpyhxde ===> fingerprint
    :param _0x10ac06: 表示地区编号
    :return: str
    """
    _0x448995 = _0x5023e1(_0x3ebd00(_0x3a5029 + '::' + _0x4c2e3c))
    _0x397f47 = f"{_0x10ac06}_{_0x448995}" if _0x10ac06 else _0x448995
    return _0x397f47 + '_v_i_1'

def get_cb():
    _0x28d664 = {
        'suffix': "m25b40",
        'code': "vfnv46",
        'pos': [1, 10, 12, 13, 26, 31],
    }
    _0x183b74 = _0x28d664
    _0x86f269 = _0x183b74['code']
    _0x22d54d = _0x183b74['pos']
    _0x58ee17 = list(uuid(32))
    for idx, _ in enumerate(_0x22d54d):
        _0x58ee17[int(_)] = _0x86f269[idx]
    return _0x3ebd00(''.join(_0x58ee17))

def get_sample(_0x4f8a50, _0x2720fb):
    _0x1f84b9 = len(_0x4f8a50)
    if _0x1f84b9 <= _0x2720fb:
        return _0x4f8a50
    _0x35f7ff = []
    _0x446efa = 0
    for _ in range(_0x1f84b9):
        if _ >= _0x446efa * (_0x1f84b9 - 1) / (_0x2720fb - 1):
            _0x35f7ff.append(_0x4f8a50[_])
            _0x446efa += 1
    return _0x35f7ff

def _0x54cf1d(x, y):
    _0x323c5c = []
    _0x36e8f3 = len(x)
    for _ in range(_0x36e8f3):
        _0x323c5c.append(_0x3346f1(x[_], y[_ % _0x36e8f3]))
    return _0x323c5c

def _0x16ff0d(_0x3741e1):
    _0x3abb26 = 'i/x1XgU0z7k8N+lCpOnPrv6\qu2Gj9HRcwTYZ4bfSJBhaWstAeoMIEQ5mDdVFLKy'
    return _0x4c4b3e(_0x3741e1, _0x3abb26, '3')

def _0x3855dc(_0x195362, _0x3ca67b):
    _0x21a5d1 = list(_0x3ca67b.encode())
    _0x321da7 = list(_0x195362.encode())
    return _0x16ff0d(_0x54cf1d(_0x21a5d1, _0x321da7))

def get_data(_0x4c7de1, start_time):
    _0x52f7fc = int(time.time() * 1000)
    _0x138504 = _0x3855dc(_0x4c7de1, ','.join([str(_) for _ in [0, 0, _0x52f7fc - (start_time if start_time else _0x52f7fc)]]))
    return json.dumps({
        'd': '',
        'm': _0x3ebd00(''),
        'p': _0x3ebd00(_0x138504),
        'ext': _0x3ebd00(_0x3855dc(_0x4c7de1, '1,0'))
    }, separators=(',', ':'))

def get_random_id():
    _0x171c6a = "0123456789abcdefghijklmnopqrstuvwxyz"
    return ''.join([random.choice(_0x171c6a) for _ in range(7)])

if __name__ == '__main__':
    # print(get_hm_lvt())
    # print(get_snaker_id())
    # print(get_gdxidpyhxde()['gdxidpyhxdE'])
    # print(len(get_ssxmod_itna()['ssxmod_itna2']))
    print(get_type_1017('https://ctbpsp.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/1?province=&industry='))
    text = "ycRtPcOVln+u8b58Lz+G8zzarso9S2bYCnPUboxUyhGnK7jRFE2PTitX6WobOKOjLM/Rt74SMUx6yOnzoZ49JChWmJhs+ypuzH2cSN1RhgtLFkjI2BcAOn1yj5RCqkBGVCx7655VELCOQJZgRyvvWrysEN/UZDoesKaYeRjEsCM=::ODDSgImoysYqc7+DXBwJPDJqrsJyaMXEQzS22WfZjxGKD0tl+QEGUqx7L3KvdIRR/UVRRv6JjN3GZ9fS\\1GttLn4WcqdOWuZbsc/9rZSh5umhbLqGcV6qKaXfluugOqrzEUehnY+Dh55jnQIQsDIUiiaLT/KN/+VNQu1UB4tZSHrU1wU:1766237912292"
    print(_0x5023e1(_0x3ebd00(text)))
