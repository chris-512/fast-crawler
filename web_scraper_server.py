#!/usr/bin/env python3 

from flask import Flask, jsonify
from bs4 import BeautifulSoup as bs
import requests_utils
from urllib import parse

from io import BytesIO

from functools import wraps, update_wrapper 
from datetime import datetime

from gevent.pywsgi import WSGIServer

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():

    return "This is Crawling Processing Server"

@app.route('/get_naver_news/url1=<url_a>&url2=<url_b>')
def getNewsContent(url_a, url_b):

    return jsonify(requests_utils.getNaverNews(url_a, url_b))

@app.route('/get_naver_news_urls/signature=<signature>')
def getNewsUrls(signature):

    return jsonify(requests_utils.getNaverNewsUrls(signature))

if __name__ == '__main__':
    WSGIServer(("127.0.0.1", 8000), app).serve_forever()