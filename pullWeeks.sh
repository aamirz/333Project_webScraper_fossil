#!/bin/bash

# silence our encoding errors 
PYTHONIOENCODING=UTF-8
export PYTHONIOENCODING

DIR="./"
#DIR='~/Documents/JuniorYear/333_COS/project/webscraper'
TOP="data_pulled"
SUM=0
# generate the date file, dates.txt in directory 
python genDateFiles.py $DIR 2017

# loop over dates.txt
while read p; do
# store the day and daydir of each line
    DAY=$(echo $p | cut -f1 -d' ')
    DAYDIR=$(echo $p | cut -f2 -d' ')
# now do the scraping and pulling for each case
    mkdir -p "${TOP}/${DAYDIR}/"
    python getTodaysArticles.py "${DIR}/${TOP}" "${DAY}"
    N=$(ls "${DIR}/${TOP}/${DAYDIR}" | wc -l)
    echo $N
    SUM=$(($SUM+$N))
    python princeToDB.py "${DIR}/${TOP}/${DAYDIR}" $N
done < dates.txt

echo "TOTAL ARTICLES PULLED: ${SUM}"
