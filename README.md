# fast-crawler

## Terminal 1
```
$ celery -A web_scraper_server.celery_app --concurrency 5 worker --loglevel=info
```
## Terminal 2 
```
$ run_server.sh
```
## Terminal 3
```
$ run.sh
```
