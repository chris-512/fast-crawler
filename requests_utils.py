from bs4 import BeautifulSoup as bs
import requests
from urllib import parse
from celery import Celery


def getNaverNewsUrls(signature, date, page):
    signature = parse.unquote(signature)
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
    page = requests.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&%s&date=%s&page=%s' % (signature, date, page), headers=headers)
    soup = bs(page.text, "html.parser")

    article_links = []
    press_names = []
    attr = {'class': 'type06_headline'}
    ul_elem = soup.find('ul', attr)
    for elem in ul_elem.find_all('dt'):
        if not elem.has_attr('class'):
            article_links.append(elem.find('a').get('href'))
    for elem in ul_elem.find_all('li'):
        press_names.append(elem.find('span', {'class': 'writing'}).text)

    attr = {'class': 'type06'}
    ul_elem = soup.find('ul', attr)
    for elem in ul_elem.find_all('dt'):
        if not elem.has_attr('class'):
            article_links.append(elem.find('a').get('href'))
    for elem in ul_elem.find_all('li'):
        press_names.append(elem.find('span', {'class': 'writing'}).text)

    return {
        'urls': article_links,
        'press_names': press_names
    }

def getNaverNewsPageNum(signature, date, page):
    signature = parse.unquote(signature)
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
    page = requests.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&%s&date=%s&page=%s' % (signature, date, page), headers=headers)
    soup = bs(page.text, "html.parser")

    attr = {'class': 'paging'}
    page_div = soup.find('div', attr)
    page_num = len(page_div.find_all('a'))

    return {
        'num_pages': page_num
    }

def call(method='', params={}):

    if method == 'get_naver_news':
        url1 = parse.quote(params['url-id1'])
        url2 = parse.quote(params['url-id2'])
        page = requests.get('http://localhost:8000/%s/url1=%s&url2=%s' % (method, url1, url2))
        return page.text
    elif method == 'get_naver_news_urls':
        signature = parse.quote(params['signature'])
        date = params['date'].strftime('%Y%m%d')
        page = params['page']
        return requests.get('http://localhost:8000/%s/signature=%s&date=%s&page=%d' % (method, signature, date, page)).text
    elif method == 'get_naver_news_num_pages':
        signature = parse.quote(params['signature'])
        date = params['date'].strftime('%Y%m%d')
        page = params['page']
        return requests.get('http://localhost:8000/%s/signature=%s&date=%s&page=%d' % (method, signature, date, page)).text

    return "Method %s Not Implemented Error" % method

if __name__ == '__main__':
    print(getNaverNewsUrls('sid2=260&sid1=101'))
    article = getNaverNews('215', '0001049298')
    print(article)