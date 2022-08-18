import requests_utils
import json
import re
import asyncio

def call_rest_api(method, params):
    json_string = requests_utils.call(method=method, params=params)
    return json.loads(json_string)

params = {
    'signature': 'sid2=260&sid1=101'
}

p = re.compile(r"https\:\/\/n.news.naver.com\/mnews\/article\/([0-9]+)\/([0-9]+)\?sid=101")

async def async_call_rest_api(params):
    res = call_rest_api(method='get_naver_news', params=params)
    for k, v in res.items():
        print('%s: %s' % (k, v))
    return True

res = call_rest_api(method='get_naver_news_urls', params=params)

url_params = []
for url in res['urls']:
    m = p.search(url)
    if m:
        print(url)

        params = {
            'url-id1': str(m.group(1)),
            'url-id2': str(m.group(2)),
        }

        url_params.append(params)

async def main():
    tasks = (async_call_rest_api(url_param) for url_param in url_params)
    L = await asyncio.gather(*tasks)
    print(L)

asyncio.run(main())