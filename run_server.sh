#!/bin/sh
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8000
export FLASK_APP=web_scraper_server.py
flask run

