#!/usr/bin/env python3 

from flask import Flask, jsonify
from bs4 import BeautifulSoup as bs
import requests
import requests_utils
from urllib import parse

from io import BytesIO

from functools import wraps, update_wrapper 
from datetime import datetime

from gevent.pywsgi import WSGIServer

from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery_app = make_celery(app)

def cleanHTMLTags(text):
    return bs(text, "lxml").text.strip()

@celery_app.task()
def getNaverNews(url_a, url_b):
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
    page = requests.get('https://n.news.naver.com/mnews/article/%s/%s?sid=101' % (str(url_a), str(url_b)), headers=headers)
    soup = bs(page.text, "html.parser")

    attr = {'id': 'dic_area'}
    elem = soup.find('div', attr)
    if elem is not None:
        article_body = cleanHTMLTags(elem.text)
    else:
        article_body = ""

    attr = {'class': 'media_end_head_info_datestamp_time'}
    elem = soup.find('span', attr)
    if elem is not None:
        article_pub_time = elem.get('data-date-time')
    else:
        article_pub_time = ""

    attr = {'class': 'media_end_head_headline'}
    elem = soup.find('h2', attr)
    if elem is not None:
        article_headline = elem.text
    else:
        article_headline = ""

    attr = {'class': 'byline_s'}
    elem = soup.find('span', attr)
    if elem is not None:
        article_author = elem.text
    else:
        article_author = ""

    return {
        'article_pub_datetime': article_pub_time,
        'article_headline': article_headline,
        'article_body': article_body,
        'article_author': article_author
    }

@app.route('/')
def index():

    return "This is Crawling Processing Server"

@app.route('/get_naver_news/url1=<url_a>&url2=<url_b>')
def getNewsContent(url_a, url_b):
    return getNaverNews.delay(url_a, url_b).id

@app.route('/get_naver_news_urls/signature=<signature>&date=<date>&page=<page>')
def getNewsUrls(signature, date, page):

    return jsonify(requests_utils.getNaverNewsUrls(signature, date, page))

@app.route('/get_naver_news_num_pages/signature=<signature>&date=<date>&page=<page>')
def getNaverNewsPageNum(signature, date, page):
    
    return jsonify(requests_utils.getNaverNewsPageNum(signature, date, page))