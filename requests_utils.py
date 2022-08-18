from bs4 import BeautifulSoup as bs
import requests
from urllib import parse

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}

def cleanHTMLTags(text):
    return bs(text, "lxml").text.strip()

def getNaverNews(url_a, url_b):
    page = requests.get('https://n.news.naver.com/mnews/article/%s/%s?sid=101' % (str(url_a), str(url_b)), headers=headers)
    soup = bs(page.text, "html.parser")

    attr = {'id': 'dic_area'}
    article_body = cleanHTMLTags(soup.find('div', attr).text)
    attr = {'class': 'media_end_head_info_datestamp_time'}
    article_pub_time = soup.find('span', attr).get('data-date-time')
    attr = {'class': 'media_end_head_headline'}
    article_headline = soup.find('h2', attr).text
    return {
        'article_pub_datetime': article_pub_time,
        'article_headline': article_headline,
        'article_body': article_body
    }

def getNaverNewsUrls(signature):
    page = requests.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&%s&page=1' % signature, headers=headers)
    soup = bs(page.text, "html.parser")

    article_links = []
    attr = {'class': 'type06_headline'}
    ul_elem = soup.find('ul', attr)
    for elem in ul_elem.find_all('dt'):
        if not elem.has_attr('class'):
            article_links.append(elem.find('a').get('href'))

    attr = {'class': 'type06'}
    ul_elem = soup.find('ul', attr)
    for elem in ul_elem.find_all('dt'):
        if not elem.has_attr('class'):
            article_links.append(elem.find('a').get('href'))

    return {
        'urls': article_links
    }


def call(method='', params={}):

    if method == 'get_naver_news':
        url1 = parse.quote(params['url-id1'])
        url2 = parse.quote(params['url-id2'])
        page = requests.get('http://localhost:5000/%s/url1=%s&url2=%s' % (method, url1, url2))
        return page.text
    elif method == 'get_naver_news_urls':
        signature = params['signature']
        page = requests.get('http://localhost:5000/%s/signature=%s' % (method, signature))
        return page.text

    return "Method %s Not Implemented Error" % method

if __name__ == '__main__':
    print(getNaverNewsUrls('sid2=260&sid1=101'))
    article = getNaverNews('215', '0001049298')
    print(article)