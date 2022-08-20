#!/bin/sh

num=5
current_date="20220820"

while [ 1 ];
do
    python3 crawler.py $current_date
    current_date=$(date -d "$current_date -5 days" +%Y%m%d)
done