#!/bin/bash
#DAY="04/03/2017"
#DAYDIR="2017_04_03"
DAY="04/13/2017"
DAYDIR="2017_04_13"

# silence stupid errors
PYTHONIOENCODING=UTF-8
export PYTHONIOENCODING

mkdir "./${DAYDIR}"
python getTodaysArticles.py "./${DAYDIR}" $DAY
# testing for local host
#python princeToDB.py "./${DAYDIR}" 12 8080

# testing to herokuapp
N="$(ls "./${DAYDIR}" | wc -l)"
echo $N
python princeToDB.py "./${DAYDIR}" $N
