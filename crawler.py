from os import scandir
import requests_utils
import json
import re
import asyncio
import concurrent
import db_helper
import functools
from sys import exit
from web_scraper_server import celery_app
from celery.result import AsyncResult

import datetime

p = re.compile(r"https\:\/\/n.news.naver.com\/mnews\/article\/([0-9]+)\/([0-9]+)\?sid=101")

def call_rest_api(method, params, is_celery_task=False):
    res = requests_utils.call(method=method, params=params)
    if is_celery_task:
        return res
    else:
        return json.loads(res)

def async_call_rest_api(params):
    task_id = call_rest_api(method='get_naver_news', params=params, is_celery_task=True)

    news = {
        'press_name': params['press_name'],
        'article_url': params['article_url'],
        'task_id': task_id
    }
    
    return news

async def crawl(datetime_str):

    params = {
        'signature': 'sid2=260&sid1=101',
        'date':  datetime.datetime.strptime(datetime_str, "%Y%m%d"),
        'page': 1
    }

    api_params = []

    print('Opening ./db/news_article_%s.db' % params['date'].strftime('%Y%m%d'))

    db_conn = db_helper.create_connection('./db/news_article_%s.db' % params['date'].strftime('%Y%m%d'))

    db_cursor = db_helper.get_cursor(db_conn)

    db_helper.create_news_table(db_conn)
    db_helper.create_urls_table(db_conn)

    for _ in range(5):

        num_pages = int(call_rest_api(method='get_naver_news_num_pages', params=params)['num_pages'])

        for i in range(1, num_pages+1):
            params['page'] = i

            res = call_rest_api(method='get_naver_news_urls', params=params)

            for url, press_name in zip(res['urls'], res['press_names']):
                m = p.search(url)
                if m:
                    
                    api_params.append({
                        'article_url': url,
                        'url-id1': str(m.group(1)),
                        'url-id2': str(m.group(2)),
                        'press_name': press_name
                    })

        params['date'] = params['date'] - datetime.timedelta(days=1) 

    #tasks = [async_call_rest_api(api_param) for api_param in api_params]
    
    import time
    st = time.time()

    #news_list = []
    #for get_news_celery_task in asyncio.as_completed(tasks):
    #   news = await get_news_celery_task
    #    news_list.append(news)

    news_list = []
    for api_param in api_params:
        time.sleep(0.05)
        news_list.append(async_call_rest_api(api_param))

    success = {}
    for news in news_list:
        task_id = news['task_id']
        press_name = news['press_name']
        article_url = news['article_url']
        res = AsyncResult(task_id, app=celery_app)
        if task_id not in success and res.state == 'SUCCESS':
            result = res.get()
            db_cursor.execute(
                'INSERT INTO news_article VALUES (?, ?, ?, ?, ?, ?)', 
                (result['article_pub_datetime'], result['article_headline'], \
                 press_name, article_url, result['article_body'], \
                 result['article_author']))
            success[task_id] = True

    ed = time.time()

    print('Number of tasks: ', len(api_params))
    print('Processed time: ', ed - st)
    print('processed time per article: ', (ed - st)/len(api_params))
    print('Number of successful downloads: ', len(success.keys()))

    db_conn.commit()

    if db_conn:
        db_conn.close()


async def main():
    import sys
    if len(sys.argv) < 2:
        exit(1)

    datetime_str = sys.argv[1]
    await crawl(datetime_str)

asyncio.run(main())