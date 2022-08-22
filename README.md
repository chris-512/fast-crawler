# fast-crawler

## Download crawled datasets
- 부동산 네이버 뉴스 데이터셋: https://drive.google.com/file/d/1gqY5Mqifkb9zz3QoIkQOaObQF_mwjZdM/view?usp=sharing

## Terminal 1
```
$ celery -A web_scraper_server.celery_app worker --concurrency 5 --loglevel=info
```
## Terminal 2 
```
$ run_server.sh
```
## Terminal 3
```
$ run.sh
```
## WORK TODO
- Python으로 pdf reader 구현, pdf에서 text 추출
- Investing.com crawl
- 통계청 crawl
- CNBC News crawl
