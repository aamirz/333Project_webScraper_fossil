#!/bin/bash
PARENTDIR=~/Documents/JuniorYear/333_COS/project/webscraper/pulled_json
TODAY="$(date "+%Y_%m_%d")"
mkdir $PARENTDIR/$TODAY
python $PARENTDIR/getTodaysArticles.py $PARENTDIR
printf "Got all Princetonian articles for %s!\n" $TODAY
