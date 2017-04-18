#!/bin/bash
DAY="04/03/2017"
DAYDIR="2017_04_03"

# silence stupid errors
PYTHONIOENCODING=UTF-8
export PYTHONIOENCODING

mkdir "./${DAYDIR}"
python getTodaysArticles.py ./ $DAY
# testing for local host
#python princeToDB.py "./${DAYDIR}" 12 8080

# testing to herokuapp
python princeToDB.py "./${DAYDIR}" 12
