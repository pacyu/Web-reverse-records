import json
import requests

cookies = {
    'abRequestId': 'fbad939c-3f6e-5738-baab-9597ebc32773',
    'webBuild': '4.86.0',
    'xsecappid': 'xhs-pc-web',
    'loadts': '1764127868001',
    'a1': '19abe370462ref6fqn748ul0rrbagahlihcg0pc5f50000324365',
    'webId': '9207b1275314b874e9c6ea4e9b9a40d1',
    'acw_tc': '0a0b11ab17641278687797948e5e90fa2ddc2fb4cb112aefc7f05f90a66792',
    'websectiga': '82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28',
    'sec_poison_id': 'ba953c66-bdc6-4772-ac88-74806cbe3e83',
    'web_session': '030037ae15200843a26c30325e2e4a7bec53cf',
    'unread': '{%22ub%22:%2264c4e818000000000800d905%22%2C%22ue%22:%2263cf9b62000000001c006b05%22%2C%22uc%22:8}',
    'gid': 'yj0DdqWy8j30yj0DdqW84xUSKJFdiKiAIW4YS2i718FFDk280k0x18888qJ4qK28i488JjYd',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.xiaohongshu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.xiaohongshu.com/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-b3-traceid': '12f07f52afe33c62',
    'x-s': 'XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIPAZlg98yGLTlqnTT/Fp9GFH7+LS1LjR9p7L3+DMw+DMawepn+FTx2bSkcDDUyfEx+7iF8rkh/Azzwr+OPoq6LgSI+bpszAQx+9QLJAmOJfl/zrhEpe+9L9RVzb4TLM+o/epl8fzkan8Pz9W3zgbL2pG6GASBN9QmPrkHaMY/+M4nzLh7PsT+c9EIqMQCLDkcpnbLP9lr4DT/Jfznnfl0yLLIaSQQyAmOarGROaHVHdWFH0ijJ9Qx8n+FHdF=',
    'x-s-common': '2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0W9N0ZjNsQh+aHCH0rEGnQSPAqI+eGUqfpf+f8lJ0qFwopVPoQUGfbdGnYVynY08AmIGApf+/ZIPeZAP0cA+0LjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/JDMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfpSL98lnLYl49IUqgcMc0mrcDShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrLUtASrpLS92dDFa/YOanS0+Mkc4FbQ4fSe+Bu6qFzP8oP9Lo4naLP78p+D+7+DPbHFaLp9qA+QzFMFpd4panSDqA+AN7+hnDESyp8FGf+p8np8pd4iag8L2fP64fp/4g4pqeSOqFzn4UTQ2BlFagYyL9RM4FRdpd4Iq7HFyBppN9L9/o8Szbm7zDS987PlqfRAPLzyyLSk+7+xGfRAP94UzDSbPo+rqg4Hag8Tnfbn4B8YLo4CanYOqFzl4MbQzLbAygb7JrSiN9prqgzm/dp7LBMn4FzQ2BMhag8zqbmDapQt/o8SP7bFyrSbzBbQyAmSngp7Lpkjzgb1PemAyfpHLFSbnLTcpd4zq7pFGLS9P9ph4gzfLrG68p8C8oPl/ok6anYdq7W7afpxLozcGS8FJFDAN7+Dqg4QanSdqAbp4gSQcFTA8B8O8Lzc4b+Q2B4A2op7+0QDpo4QzLc3aLP9q7YQJ9pn804S8oQOqMSc4okQypZlag8Tybkn4BRQc9lxanYdqM8P+BlHpaRA8dbF4rSi/emEpdqUJ9z68nTS8o+hpdzmPdpFzDSkzMbQ4S+BLobF+9Ql4A+QyFEAP9r98nzn4FDULocAag83+FEl4bmQ2bqE8/miJFSk8o+x/g8APB8O8nSM49bTLoc3anSnNFSh+d+hLozpaLP7q9krqSpQ4fYOJMDhzrShyURQ2rbAyMm7yURn4AzOn0FRHjIj2eDjwjFlPeHIPePEPeW7NsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR',
    'x-t': '1764127892468',
    'x-xray-traceid': 'cd5f1bb1f41d7b47e972520565734245',
    'xy-direction': '15',
    # 'cookie': 'abRequestId=fbad939c-3f6e-5738-baab-9597ebc32773; webBuild=4.86.0; xsecappid=xhs-pc-web; loadts=1764127868001; a1=19abe370462ref6fqn748ul0rrbagahlihcg0pc5f50000324365; webId=9207b1275314b874e9c6ea4e9b9a40d1; acw_tc=0a0b11ab17641278687797948e5e90fa2ddc2fb4cb112aefc7f05f90a66792; websectiga=82e85efc5500b609ac1166aaf086ff8aa4261153a448ef0be5b17417e4512f28; sec_poison_id=ba953c66-bdc6-4772-ac88-74806cbe3e83; web_session=030037ae15200843a26c30325e2e4a7bec53cf; unread={%22ub%22:%2264c4e818000000000800d905%22%2C%22ue%22:%2263cf9b62000000001c006b05%22%2C%22uc%22:8}; gid=yj0DdqWy8j30yj0DdqW84xUSKJFdiKiAIW4YS2i718FFDk280k0x18888qJ4qK28i488JjYd',
}

json_data = {
    'cursor_score': '',
    'num': 18,
    'refresh_type': 1,
    'note_index': 18,
    'unread_begin_note_id': '',
    'unread_end_note_id': '',
    'unread_note_count': 0,
    'category': 'homefeed.movie_and_tv_v3',
    'search_key': '',
    'need_num': 8,
    'image_formats': [
        'jpg',
        'webp',
        'avif',
    ],
    'need_filter_image': False,
}

response = requests.post('https://edith.xiaohongshu.com/api/sns/web/v1/homefeed', cookies=cookies, headers=headers, data=json.dumps(json_data, separators=(',', ':')))

print(response.text)
