const wasm = require("./webet.js");

async function encrypt(data) {
  await wasm.default();
  return await wasm.wet(JSON.stringify(data));
}

async function decrypt(data) {
  await wasm.default();
  return await JSON.parse(wasm.wdt(data));
}

(async () => {
  const url = "https://www.yzczb.com/portal-site-api/notice/website/page";
  const data = { "projectClassification": 1, "projectTypeCode": 0, "releaseTimeType": 0, "category": 0, "areaCode": "0", "pageParam": { "pageNum": 1, "pageSize": 15 } };

  const encrypt_data = await encrypt(data);

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json;charset=UTF-8',
      'Origin': 'https://www.yzczb.com',
      'Pragma': 'no-cache',
      'Referer': 'https://www.yzczb.com/site-search?pType=1',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'Cookie': 'Hm_lvt_259f7e4c7cfb117a79b947aec5d869ff=1765537680; Hm_lpvt_259f7e4c7cfb117a79b947aec5d869ff=1765537680; HMACCOUNT=C273E157027E82D7'
    },
    body: encrypt_data,
  })
  if (!response.ok) {
    throw new Error(`HTTP 错误！状态码: ${response.status}`);
  }
  const encrypt_result = await response.text();
  let result = await decrypt(encrypt_result);
  console.log(result);
})();
